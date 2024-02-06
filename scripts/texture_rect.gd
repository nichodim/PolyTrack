extends TextureRect

@onready var saved_texture = texture

func _get_drag_data(at_position):
	var preview_texture = TextureRect.new()
	
	preview_texture.texture = texture
	preview_texture.expand_mode = 1
	preview_texture.size = Vector2(30,30)
	
	var preview = Control.new()
	preview.add_child(preview_texture)
	preview_texture.position = -0.5 * preview_texture.size
	set_drag_preview(preview)
	texture = null
	
	return preview_texture.texture
 
func _can_drop_data(_pos, data):
	return data is Texture2D
 
func _drop_data(_pos, data):
	texture = data

func _notification(what: int) -> void:
	if what == NOTIFICATION_DRAG_END and not self.is_drag_successful():
		texture = saved_texture
