use ort::session::{builder::GraphOptimizationLevel, Session};

fn main() -> ort::error::Result<()> {
    println!("Hello, Adrien!");

    let model_path = "yolov8m.onnx";
    let model = Session::builder()?
        .with_optimization_level(GraphOptimizationLevel::Level3)?
        .with_intra_threads(4)?
        .commit_from_file(model_path)?;

    println!("Model {model_path} loaded successfully!");
    println!("Model: {:?}", model);

    Ok(())
}
