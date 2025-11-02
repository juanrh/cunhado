import pytest
from pathlib import Path
import tempfile
import os

from cunhado.config import ModelProvider, Settings, get_settings_from_yaml


def test_model_provider_enum():
    """Test that the ModelProvider enum works correctly."""
    # Test enum values
    assert ModelProvider.MISTRAL.value == "mistral"
    assert ModelProvider.OPENROUTER.value == "openrouter"
    
    # Test string representation
    assert str(ModelProvider.MISTRAL) == "ModelProvider.MISTRAL"
    assert str(ModelProvider.OPENROUTER) == "ModelProvider.OPENROUTER"


def test_settings_validation():
    """Test that Settings validation works correctly."""
    # Test valid settings
    settings_mistral = Settings(model_provider=ModelProvider.MISTRAL)
    assert settings_mistral.model_provider == ModelProvider.MISTRAL
    
    settings_openrouter = Settings(model_provider=ModelProvider.OPENROUTER)
    assert settings_openrouter.model_provider == ModelProvider.OPENROUTER
    
    # Test that model_provider is mandatory (no default)
    with pytest.raises(Exception):
        Settings()  # Should fail without model_provider


def test_yaml_loading_mistral():
    """Test YAML file loading with mistral provider."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write('model_provider: "mistral"\n')
        f.flush()
        
        settings = get_settings_from_yaml(Path(f.name))
        assert settings.model_provider == ModelProvider.MISTRAL
    
    # Clean up
    os.unlink(f.name)


def test_yaml_loading_openrouter():
    """Test YAML file loading with openrouter provider."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write('model_provider: "openrouter"\n')
        f.flush()
        
        settings = get_settings_from_yaml(Path(f.name))
        assert settings.model_provider == ModelProvider.OPENROUTER
    
    # Clean up
    os.unlink(f.name)


def test_yaml_loading_invalid_provider():
    """Test YAML file loading with invalid provider."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write('model_provider: "invalid"\n')
        f.flush()
        
        with pytest.raises(Exception):
            get_settings_from_yaml(Path(f.name))
    
    # Clean up
    os.unlink(f.name)


def test_yaml_loading_missing_file():
    """Test YAML file loading with non-existent file."""
    with pytest.raises(Exception):
        get_settings_from_yaml(Path("/nonexistent/file.yaml"))
