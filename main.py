from sanbproject.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    training_pipeline = TrainingPipeline()
    training_pipeline.trigger_training_pipeline()