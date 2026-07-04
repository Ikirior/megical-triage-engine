from services.medgemma import MedGemmaProvider, MedGemmaProviderMock
import os

def create_medgemma():
    use_model = os.getenv("USE_MODEL", "mock")

    if use_model == 'local' or use_model == 'cloud':
        return MedGemmaProvider
    else:
        return MedGemmaProviderMock