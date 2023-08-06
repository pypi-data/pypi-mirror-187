use bevy_reflect::serde::ReflectSerializer;
use bevy_reflect::{DynamicStruct, Reflect, TypeRegistry};
use bevy_transform::components::Transform;
use glam::{Quat, Vec3};
use pyo3::prelude::*;

/// <Vector (0, 1, 2)>
#[derive(FromPyObject)]
pub struct Vector(f32, f32, f32);

impl Vector {
    fn to_vec3(self) -> Vec3 {
        Vec3::new(self.0, self.1, self.2)
    }
}

/// <Quaternion (w=0, x=1, y=2, z=3)>
#[derive(FromPyObject)]
pub struct Quaternion(f32, f32, f32, f32);

impl Quaternion {
    fn to_quat(self) -> Quat {
        Quat::from_xyzw(self.3, self.2, self.1, self.0)
    }
}

/// Serializes transform into ron string.
#[pyfunction]
pub fn transform_ron(transform: Vector, rotation: Quaternion, scale: Vector) -> PyResult<String> {
    let mut type_registry = TypeRegistry::default();
    type_registry.register::<Quat>();

    let mut value = Transform::from_translation(transform.to_vec3());
    value.rotation = rotation.to_quat();
    value.scale = scale.to_vec3();

    let patch = DynamicStruct::default();
    value.apply(&patch);

    let serializer = ReflectSerializer::new(&value, &type_registry);
    let ron_string =
        ron::ser::to_string_pretty(&serializer, ron::ser::PrettyConfig::default()).unwrap();
    Ok(ron_string)
}

/// A Python module implemented in Rust.
#[pymodule]
fn bevy_adapter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(transform_ron, m)?)?;
    Ok(())
}
