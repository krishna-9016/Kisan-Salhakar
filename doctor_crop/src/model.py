import torch
import torch.nn as nn
from torchvision import models


def create_model(num_classes, pretrained=True):
    """
    Creates an EfficientNet-B0 model with a custom classifier.

    Args:
        num_classes (int): The number of output classes for the final layer.
        pretrained (bool): Whether to use pre-trained weights from ImageNet.

    Returns:
        A PyTorch model instance.
    """
    # Load the pre-trained EfficientNet-B0 model
    if pretrained:
        weights = models.EfficientNet_B0_Weights.IMAGENET1K_V1
    else:
        weights = None

    model = models.efficientnet_b0(weights=weights)

    # Freeze all the parameters in the pre-trained model
    for param in model.parameters():
        param.requires_grad = False

    # Replace the final classifier layer
    # EfficientNet's classifier is at 'model.classifier[1]'
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(
        in_features=num_features, out_features=num_classes)

    return model


if __name__ == '__main__':
    # This block is for testing the function directly
    # It will only run when you execute "python src/model.py"
    NUM_CLASSES = 38
    my_model = create_model(NUM_CLASSES)

    # Print the model's classifier to verify the change
    print("--- Model Test ---")
    print("Successfully created a model.")
    print("\nModel's classifier structure:")
    print(my_model.classifier)

    # Create a dummy input tensor and pass it through the model
    dummy_input = torch.randn(1, 3, 224, 224)
    output = my_model(dummy_input)
    print(f"\nOutput shape for a dummy input: {output.shape}")
    print(f"Expected output shape: (1, {NUM_CLASSES})")
