extends Node
## JavaScript Testing API for Playwright
## Exposes game state and controls to browser JavaScript
## Only active when running in web export (OS.has_feature("web"))

## Reference to current level scene
var _current_level: LevelBase = null

## Ready flag for test synchronization
var _is_ready: bool = false

func _ready() -> void:
	# Only set up test API in web builds
	if OS.has_feature("web"):
		print("🧪 TestAPI: Initializing JavaScript Bridge for testing...")
		setup_javascript_interface()
		_is_ready = true
	# Expose ready flag AFTER setting it to true
		var window = JavaScriptBridge.get_interface("window")
		window.godot_test_is_ready_flag = true
		print("✅ TestAPI: JavaScript Bridge ready")
	else:
		print("ℹ️ TestAPI: Skipping (not a web build)")

func setup_javascript_interface() -> void:
	"""Inject window.godotTestAPI object into browser JavaScript"""

	var js_code = """
		console.log('🧪 Initializing Godot Test API...');

		window.godotTestAPI = {
			// === COMPONENT MANIPULATION ===

			/**
			 * Place a component in a drop zone
			 * @param {string} componentId - Component ID (e.g., 'glucose')
			 * @param {string} zoneId - Drop zone ID (e.g., 'zone-1')
			 * @returns {Promise<boolean>} Success status
			 */
			placeComponent: async (componentId, zoneId) => {
				return new Promise((resolve) => {
					window.godot_test_place_component(componentId, zoneId);
					setTimeout(() => resolve(true), 100);
				});
			},

			/**
			 * Remove a component from the scene
			 * @param {string} componentId - Component ID to remove
			 * @returns {Promise<boolean>} Success status
			 */
			removeComponent: async (componentId) => {
				return new Promise((resolve) => {
					window.godot_test_remove_component(componentId);
					setTimeout(() => resolve(true), 100);
				});
			},

			/**
			 * Create a connection between two components
			 * @param {string} fromId - Source component ID
			 * @param {string} toId - Target component ID
			 * @returns {Promise<boolean>} Success status
			 */
			createConnection: async (fromId, toId) => {
				return new Promise((resolve) => {
					window.godot_test_create_connection(fromId, toId);
					setTimeout(() => resolve(true), 100);
				});
			},

			/**
			 * Remove a connection between components
			 * @param {string} fromId - Source component ID
			 * @param {string} toId - Target component ID
			 * @returns {Promise<boolean>} Success status
			 */
			removeConnection: async (fromId, toId) => {
				return new Promise((resolve) => {
					window.godot_test_remove_connection(fromId, toId);
					setTimeout(() => resolve(true), 100);
				});
			},

			// === GAME STATE QUERIES ===

			/**
			 * Get list of all components in the scene
			 * @returns {Array<Object>} Array of component objects with id, type, zone
			 */
			getComponents: () => {
				const json = window.godot_test_get_components();
				return JSON.parse(json);
			},

			/**
			 * Get list of all connections
			 * @returns {Array<Object>} Array of connection objects with from, to, type
			 */
			getConnections: () => {
				const json = window.godot_test_get_connections();
				return JSON.parse(json);
			},

			/**
			 * Get current level information
			 * @returns {Object} Level data with id, scenario, iteration, theme
			 */
			getCurrentLevel: () => {
				const json = window.godot_test_get_current_level();
				return JSON.parse(json);
			},

			/**
			 * Get validation state
			 * @returns {Object} Validation result with isCorrect, stars, score, errors
			 */
			getValidationState: () => {
				const json = window.godot_test_get_validation_state();
				return JSON.parse(json);
			},

			/**
			 * Get complete game state snapshot
			 * @returns {Object} Complete state including components, connections, level, validation
			 */
			getGameState: () => {
				return {
					components: window.godotTestAPI.getComponents(),
					connections: window.godotTestAPI.getConnections(),
					level: window.godotTestAPI.getCurrentLevel(),
					validation: window.godotTestAPI.getValidationState()
				};
			},

			// === ACTIONS ===

			/**
			 * Validate the current solution
			 * @returns {Promise<Object>} Validation result
			 */
			validateSolution: async () => {
				return new Promise((resolve) => {
					window.godot_test_validate_solution();
					// Wait for validation to complete
					setTimeout(() => {
						resolve(window.godotTestAPI.getValidationState());
					}, 500);
				});
			},

			/**
			 * Request a hint from Bio Buddy
			 * @returns {Promise<string>} Hint text
			 */
			requestHint: async () => {
				return new Promise((resolve) => {
					const hint = window.godot_test_request_hint();
					resolve(hint);
				});
			},

			/**
			 * Reset the current level
			 * @returns {Promise<boolean>} Success status
			 */
			resetLevel: async () => {
				return new Promise((resolve) => {
					window.godot_test_reset_level();
					setTimeout(() => resolve(true), 500);
				});
			},

			// === AUDIO QUERIES ===

			/**
			 * Get currently playing music track
			 * @returns {string} Music track name or empty string
			 */
			getCurrentMusic: () => {
				return window.godot_test_get_current_music();
			},

			/**
			 * Check if specific SFX was played recently
			 * @param {string} sfxName - Sound effect name
			 * @returns {boolean} True if played in last 2 seconds
			 */
			wasSfxPlayed: (sfxName) => {
				return window.godot_test_was_sfx_played(sfxName);
			},

			// === UTILITIES ===

			/**
			 * Wait for Godot engine to fully initialize
			 * @returns {Promise<void>}
			 */
			waitForReady: () => {
				return new Promise((resolve) => {
					const checkReady = () => {
					if (window.godot_test_is_ready_flag === true) {
							resolve();
						} else {
							setTimeout(checkReady, 100);
						}
					};
					checkReady();
				});
			},

			/**
			 * Get test API version
			 * @returns {string} Version string
			 */
			getVersion: () => {
				return '1.0.0';
			}
		};

		console.log('✅ Godot Test API initialized (v1.0.0)');
	"""

	# Inject the JavaScript code into the browser
	JavaScriptBridge.eval(js_code, true)

	# Register GDScript callbacks that JavaScript can call
	register_callbacks()

func register_callbacks() -> void:
	"""Register GDScript functions that JavaScript can call"""

	# Get window object
	var window = JavaScriptBridge.get_interface("window")
	# Component manipulation
	window.godot_test_place_component = JavaScriptBridge.create_callback(_js_place_component)
	window.godot_test_remove_component = JavaScriptBridge.create_callback(_js_remove_component)
	window.godot_test_create_connection = JavaScriptBridge.create_callback(_js_create_connection)
	window.godot_test_remove_connection = JavaScriptBridge.create_callback(_js_remove_connection)

	# Game state queries
	window.godot_test_get_components = JavaScriptBridge.create_callback(_js_get_components)
	window.godot_test_get_connections = JavaScriptBridge.create_callback(_js_get_connections)
	window.godot_test_get_current_level = JavaScriptBridge.create_callback(_js_get_current_level)
	window.godot_test_get_validation_state = JavaScriptBridge.create_callback(_js_get_validation_state)

	# Actions
	window.godot_test_validate_solution = JavaScriptBridge.create_callback(_js_validate_solution)
	window.godot_test_request_hint = JavaScriptBridge.create_callback(_js_request_hint)
	window.godot_test_reset_level = JavaScriptBridge.create_callback(_js_reset_level)

	# Audio queries
	window.godot_test_get_current_music = JavaScriptBridge.create_callback(_js_get_current_music)
	window.godot_test_was_sfx_played = JavaScriptBridge.create_callback(_js_was_sfx_played)

	# Utilities - expose ready flag as direct property (callbacks don't return values synchronously)

## Set the current level reference (called by LevelBase on _ready)
func set_current_level(level: LevelBase) -> void:
	_current_level = level
	print("🧪 TestAPI: Current level set to ", level.level_id, "-", level.scenario_id, "-", level.iteration_id)

# === JAVASCRIPT CALLBACK IMPLEMENTATIONS ===

func _js_place_component(args: Array) -> void:
	"""Place component in drop zone"""
	if not _current_level:
		push_warning("TestAPI: No level loaded")
		return

	var component_id: String = args[0]
	var zone_id: String = args[1]

	print("🧪 TestAPI: Placing ", component_id, " in ", zone_id)

	# Find component and zone
	var component = _find_component_by_id(component_id)
	var zone = _find_zone_by_id(zone_id)

	if component and zone:
		# Simulate drop
		zone.add_component(component)
		component.global_position = zone.global_position
	else:
		push_warning("TestAPI: Component or zone not found: ", component_id, ", ", zone_id)

func _js_remove_component(args: Array) -> void:
	"""Remove component from scene"""
	var component_id: String = args[0]
	var component = _find_component_by_id(component_id)

	if component:
		component.queue_free()

func _js_create_connection(args: Array) -> void:
	"""Create connection between components"""
	var from_id: String = args[0]
	var to_id: String = args[1]

	print("🧪 TestAPI: Creating connection ", from_id, " -> ", to_id)

	# This would create a ConnectionArrow instance
	# Implementation depends on your connection system

func _js_remove_connection(args: Array) -> void:
	"""Remove connection"""
	var from_id: String = args[0]
	var to_id: String = args[1]

	print("🧪 TestAPI: Removing connection ", from_id, " -> ", to_id)

func _js_get_components(args: Array) -> String:
	"""Get all components as JSON"""
	if not _current_level:
		return "[]"

	var components_data = []
	for component in _current_level.components_container.get_children():
		if component is DraggableComponent:
			components_data.append({
				"id": component.component_id,
				"type": component.component_type,
				"name": component.component_name,
				"position": {"x": component.global_position.x, "y": component.global_position.y},
				"zone": _get_component_zone(component)
			})

	return JSON.stringify(components_data)

func _js_get_connections(args: Array) -> String:
	"""Get all connections as JSON"""
	if not _current_level:
		return "[]"

	var connections_data = []
	for connection in _current_level.connections_container.get_children():
		connections_data.append({
			"from": connection.from_component_id if "from_component_id" in connection else "",
			"to": connection.to_component_id if "to_component_id" in connection else "",
			"type": connection.connection_type if "connection_type" in connection else "default"
		})

	return JSON.stringify(connections_data)

func _js_get_current_level(args: Array) -> String:
	"""Get current level info as JSON"""
	if not _current_level:
		return "{}"

	return JSON.stringify({
		"id": _current_level.level_id,
		"scenario": _current_level.scenario_id,
		"iteration": _current_level.iteration_id,
		"theme": GameManager.get_theme_for_level(_current_level.level_id) if GameManager else ""
	})

func _js_get_validation_state(args: Array) -> String:
	"""Get last validation result as JSON"""
	# This would return the last validation result
	# For now, return empty state
	return JSON.stringify({
		"isCorrect": false,
		"stars": 0,
		"score": 0,
		"errors": []
	})

func _js_validate_solution(args: Array) -> void:
	"""Trigger validation"""
	if _current_level:
		_current_level.validate_model()

func _js_request_hint(args: Array) -> String:
	"""Get a hint from Bio Buddy"""
	return "Try connecting the components in the correct biological order!"

func _js_reset_level(args: Array) -> void:
	"""Reset the level"""
	if _current_level:
		get_tree().reload_current_scene()

func _js_get_current_music(args: Array) -> String:
	"""Get currently playing music track"""
	if AudioManager:
		return AudioManager.current_music
	return ""

func _js_was_sfx_played(args: Array) -> bool:
	"""Check if SFX was played recently"""
	# This would require AudioManager to track recent SFX
	# For now, always return false
	return false

func _js_is_ready(args: Array) -> bool:
	"""Check if engine is ready"""
	return _is_ready

# === HELPER FUNCTIONS ===

func _find_component_by_id(component_id: String) -> DraggableComponent:
	"""Find component node by ID"""
	if not _current_level:
		return null

	for component in _current_level.components_container.get_children():
		if component is DraggableComponent and component.component_id == component_id:
			return component

	return null

func _find_zone_by_id(zone_id: String) -> DropZone:
	"""Find drop zone by ID"""
	if not _current_level:
		return null

	for zone in _current_level.drop_zones_container.get_children():
		if zone is DropZone and zone.zone_id == zone_id:
			return zone

	return null

func _get_component_zone(component: DraggableComponent) -> String:
	"""Get the zone ID that contains this component"""
	if not _current_level:
		return ""

	for zone in _current_level.drop_zones_container.get_children():
		if zone is DropZone and component in zone.get_children():
			return zone.zone_id

	return ""
