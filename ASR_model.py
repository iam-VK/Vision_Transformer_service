import torch
import torchaudio
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import soundfile as sf
from MY_modules import file_name_extract

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

def load_model(model_id):
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
                                            model_id, 
                                            torch_dtype=torch_dtype, 
                                            low_cpu_mem_usage=True
    )
    processor = AutoProcessor.from_pretrained(model_id)
    model.to(device)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=30,
        batch_size=16,
        torch_dtype=torch_dtype,
        device=device,
    )

    return pipe

def load_audio(file_path, target_sample_rate=16000):
    waveform, sample_rate = sf.read(file_path)
    waveform = torch.tensor(waveform, dtype=torch.float32)
    
    # Ensure the audio is mono by averaging channels if necessary
    if waveform.ndim > 1:
        waveform = torch.mean(waveform, dim=1)
     
    # Resample if necessary to 16000
    if sample_rate != target_sample_rate:
        transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)
        waveform = transform(waveform.unsqueeze(0)).squeeze(0)
    
    return waveform

def speech_recog(filename):
    _, filename = file_name_extract(filename)
    audio = load_audio(file_path=f"./audios/{filename}.wav")

    # Convert the PyTorch Tensor to a NumPy ndarray
    audio_numpy = audio.numpy()

    model_id = "Models/whisper-medium"
    pipe = load_model(model_id)

    result = pipe(audio_numpy)
    transcription = result["text"]
    return transcription