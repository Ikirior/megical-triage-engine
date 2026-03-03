from services.medgemma import MedGemmaProvider, MedGemmaProviderMock, MedGemmaProviderCloud
import os

def create_medgemma():
    use_model = os.getenv("USE_MODEL", "mock")

    if use_model == 'local':
        return MedGemmaProvider
    elif use_model == 'cloud':
        return MedGemmaProviderCloud
    else:
        return MedGemmaProviderMock