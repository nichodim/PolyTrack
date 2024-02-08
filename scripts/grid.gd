extends Node

@export var tile_scene: PackedScene

@export var columns = 1150/50 + 1
@export var rows = 8
@export var tile_size = 50
# Called when the node enters the scene tree for the first time.
func _ready():
	var grid = GridContainer.new()
	grid.columns = columns
	
	grid.position = Vector2(1.0, 0.0)
	grid.add_theme_constant_override("h_separation", 0)
	grid.add_theme_constant_override("v_separation", 0)
	
	for i in range(columns * rows):
		var tile = tile_scene.instantiate()
		tile.size = Vector2(100.0, 100.0)
		tile.child_entered_tree
		grid.add_child(tile)
	add_child(grid)
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
