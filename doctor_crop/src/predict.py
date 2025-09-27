import torch
import argparse
import pandas as pd
from PIL import Image
from torchvision import transforms

# Import our custom modules
from model import create_model


def predict(image_path, model_path, data_dir):
    """
    Makes a prediction on a single image using a trained model.

    Args:
        image_path (str): Path to the input image.
        model_path (str): Path to the saved .pth model file.
        data_dir (str): Path to the 'data/processed' directory to load mappings.
    """
    # --- 1. Setup ---
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # --- 2. Load Mappings ---
    # We need the class-to-index mapping from the training phase to decode predictions.
    # The best way is to recreate it from the saved training data.
    train_df = pd.read_parquet(f'{data_dir}/train.parquet')
    class_to_idx = {label: i for i, label in enumerate(
        train_df['label'].unique())}
    idx_to_class = {i: label for label, i in class_to_idx.items()}
    num_classes = len(class_to_idx)

    # --- 3. Load Model ---
    model = create_model(num_classes=num_classes, pretrained=False)
    # Load the trained weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()  # Set model to evaluation mode

    # --- 4. Prepare Image ---
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image = Image.open(image_path).convert("RGB")
    # Apply transformations and add a batch dimension (B, C, H, W)
    image_tensor = transform(image).unsqueeze(0).to(device)

    # --- 5. Make Prediction ---
    with torch.no_grad():
        output = model(image_tensor)
        # Apply softmax to get probabilities
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        # Get the top prediction
        top_prob, top_idx = torch.max(probabilities, 0)

    pred_class_name = idx_to_class[top_idx.item()]
    pred_confidence = top_prob.item()

    # --- 6. Display Result ---
    print("\n--- Prediction Result ---")
    print(
        f"Predicted Disease: {pred_class_name.split('___')[1].replace('_', ' ')}")
    print(f"Confidence: {pred_confidence * 100:.2f}%")


if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Predict a plant disease from an image.")
    parser.add_argument('--image_path', type=str,
                        required=True, help='Path to the input image.')

    # **FIX:** Remove the '../' from the default paths.
    # The script should look for these files from the project's root directory.
    parser.add_argument('--model_path', type=str,
                        default='best_crop_doctor_model.pth', help='Path to the saved model file.')
    parser.add_argument('--data_dir', type=str, default='data/processed',
                        help='Path to the processed data directory.')

    args = parser.parse_args()

    # Run the prediction function
    predict(args.image_path, args.model_path, args.data_dir)
