import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import torch

# 1. Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Toxicity Guardian API", version="2.0.0")
print("\n\n 🚀 NEW CODE LOADED: BLACKLIST ACTIVE! 🚀 \n\n")

# 2. CORS Security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# 3. Load Multilingual AI Model (Hinglish/Hindi/English)
MODEL_NAME = "unitary/multilingual-toxic-xlm-roberta"
logger.info(f"Loading {MODEL_NAME}... this may take a moment.")

try:
    device = 0 if torch.cuda.is_available() else -1
    classifier = pipeline("text-classification", model=MODEL_NAME, top_k=None, device=device)
    logger.info("✅ Multilingual Model loaded successfully.")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")
    classifier = None

# ==============================================================================
# 4. MASSIVE HINGLISH & ENGLISH BLACKLIST (The "Instant Ban" List)
# ==============================================================================
HINGLISH_BLACKLIST = [
    # --- LEVEL 1: Common Insults (Hinglish) ---
    "pagal", "paagal", "gadha", "gadhha", "ullu", "bewakoof", "bewaquf",
    "nalayak", "nalla", "chapri", "chhapri", "chammak", "dhakkan", "lukkha",
    "fattu", "bhikari", "bikhari", "ganwar", "gavar", "dehati", "jahil",
    "bakwaas", "bakwas", "bekar", "ghatia", "ghatiya", "ganda", "gandi",
    "kuda", "kachra", "tatti", "potty", "hag", "hagga",

    # --- LEVEL 2: Animal Insults ---
    "kutta", "kute", "kuta", "kutte", "kutiya", "kutiyaa",
    "kamina", "kamine", "kaminay", "suar", "suwar", "janwar",
    "bhens", "bhains", "bandar", "langoor", "khota",

    # --- LEVEL 3: Severe Abuses (Cursing/Swearing) ---
    "saala", "sala", "saale", "saley", "haramkhor", "harami", "haraami",
    "chutiya", "chu", "chutye", "choot", "chut",
    "gandu", "gaandu", "gand", "gaand", "gandfata", "gandmra",
    "bhosdike", "bhosadike", "bsdk", "bhosda",
    "madarchod", "mc", "ma ki", "maa ki", "maderchod",
    "bhenchod", "bc", "behenchod", "behen ki",
    "lawde", "lavde", "laude", "loda", "lowda", "lund", "land",
    "randi", "rand", "randwa", "chinal", "raand",
    "hijra", "chakka", "meetha", "halala", "kafir",

    # --- LEVEL 4: Phrases & Sentences (Hinglish) ---
    "dimaag kharab", "dimag kharab", "khopdi", "bheja fry",
    "chup kar", "chup be", "shakal dekh", "aukat", "auqaat",
    "mar ja", "marja", "doob mar", "nikal", "dafa ho",
    "baap par", "baap pe", "teri maa", "teri behen",

    # --- LEVEL 5: English Common Toxic Words ---
    "idiot", "stupid", "dumb", "fool", "moron", "retard", "loser",
    "useless", "pathetic", "disgusting", "nonsense", "rubbish", "trash",
    "shut up", "get lost", "go to hell", "kill yourself", "kys",
    "fuck", "fucker", "fucking", "shit", "bullshit", "bitch", "bastard",
    "asshole", "dick", "pussy", "cunt", "whore", "slut", "rapist"
]

# MASSIVE HINDI (DEVANAGARI) LIST - 200+ Words
HINDI_BLACKLIST = [
    # --- Category 1: Intelligence & Competence ---
    "पागल", "पगला", "बौरा", "सनकी", "सठिया", "खिसका", "दिमाग से पैदल",
    "बेवकूफ", "मूर्ख", "जाहिल", "गंवार", "अनपढ़", "बुद्धू", "मंदबुद्धि",
    "गधा", "गधे", "उल्लू", "उल्लू का पट्ठा", "बैल बुद्धि", "गोबर गणेश",
    "नालायक", "नाकाम", "नल्ला", "निठल्ला", "कामचोर", "फालतू",
    "ढक्कन", "लोल", "चूतिया", "अकल के दुश्मन",

    # --- Category 2: Character & Integrity ---
    "कमीना", "कमीने", "हरामखोर", "हरामी", "नीच", "धूर्त", "पापी",
    "धोखेबाज", "मक्कार", "झूठा", "फरेबी", "दलाल", "भड़वा", "कुकर्मी",
    "दुष्ट", "राक्षस", "शैतान", "दरिंदा", "हैवान", "जल्लाद",
    "बेगैरत", "बेशर्म", "बेहया", "नमकहराम", "गद्दार", "कुलच्छनी",

    # --- Category 3: Class & Appearance (Slurs) ---
    "छपरी", "छमिय", "भिखारी", "भीख", "कंजूस", "मक्खीचूस",
    "देहाती", "देहाती गवार", "काला", "कलुआ", "मोटा", "हाथी", "संडा",
    "टिड्डी", "सूखा", "हड्डी", "बौना", 

    # --- Category 4: Filth & Disgust ---
    "बकवास", "बेकार", "कचरा", "कूड़ा", "गंदा", "गंदी", "घटिया",
    "सड़ा", "बदबूदार", "कीड़ा", "नाली का कीड़ा", "गंदगी",
    "टट्टी", "गोबर", "हग", "हग्गा", "मूत्र", "पेशाब",

    # --- Category 5: Animals (Used as insults) ---
    "कुत्ता", "कुत्ते", "कुतिया", "पिल्ला", "सूअर", "सुअर", 
    "जानवर", "भेड़िया", "सांप", "नेवला", "बंदर", "लंगूर",
    "भैंस", "गेंडा", "खच्चर",

    # --- Category 6: Severe Vulgarity (Body Parts/Acts) ---
    "गांड", "गांडू", "गाँड", "गाण्ड", "पिछवाड़ा", "चूत", "चूतिया", "चूतिये",
    "भोसड़ा", "भोसड़ी", "भोसड़ीवाला", "भोसड़ीवाले", "भोसडी",
    "लंड", "लौड़ा", "लवडा", "लिंग", "झांट", "झाटू", "बाल",
    "चोद", "चोदू", "चोदना", "चुदाई", "मुठल", "हिलाने वाला",
    "गांडमरा", "गांडफटा", "चूतड़",

    # --- Category 7: Severe Abuses (Relations) ---
    "मादरचोद", "मादर", "माँ की", "तेरी माँ की",
    "बहनचोद", "बेहनचोद", "बहन की", "तेरी बहन की",
    "बेटीचोद", "बाप पर मत जा", "रंडी", "रन्डी", "छिनाला", "छिनाल",
    "तवायफ", "कोठेवाली", "धंधेवाली", "नाजायज", "हराम की औलाद",

    # --- Category 8: Identity Slurs (Gender/Orientation) ---
    "हिजड़ा", "छक्का", "मीठा", "गुड़बाज", "नामर्द", "नपुंसक", 

    # --- Category 9: Violence & Threats ---
    "साला", "साले", "साली", "मर जा", "दफा हो", "निकल", "भाग",
    "औकात", "औकात में रह", "तेरी औकात", "फोड़ दूंगा", "तोड़ दूंगा",
    "जान से मार", "मार डालूंगा", "काट डालूंगा", "चीर दूंगा", "जिंदा जला",
    "खून पी जाऊंगा", "टांग तोड़", "मुंह तोड़", "थोबड़ा"
]

class AnalysisRequest(BaseModel):
    text: str
    threshold: float = 0.05  # Very sensitive AI threshold

@app.get("/health")
def health_check():
    return {"status": "active", "model": MODEL_NAME}

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    if not classifier:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # 1. Clean the text for checking
    text_lower = request.text.lower()
    
    # 2. CHECK BLACKLIST FIRST (Instant Ban)
    for bad_word in HINGLISH_BLACKLIST:
        # We check if the bad word is "in" the text. 
        # For better accuracy, we can check word boundaries, but simple 'in' works for now.
        if bad_word in text_lower:
            print(f"🚫 BLOCKED by Blacklist: Found '{bad_word}' in '{request.text[:20]}...'")
            return {
                "is_toxic": True,
                "categories": ["insult (manual blocklist)"]
            }

    # 3. IF SAFE FROM BLACKLIST, CHECK AI
    try:
        safe_text = request.text[:2000]
        results = classifier(safe_text)[0]

        toxic_categories = []
        is_toxic = False

        print(f"\n🧐 AI Analyzing: '{safe_text[:30]}...'")
        for res in results:
            print(f"   -> Label: {res['label']}, Score: {res['score']:.4f}")
            
            # If AI is confident it's toxic
            if res['label'] != 'neutral' and res['score'] >= request.threshold:
                toxic_categories.append(res['label'])
                is_toxic = True
        
        print(f"   => AI VERDICT: {'TOXIC 🔴' if is_toxic else 'SAFE 🟢'}")

        return {
            "is_toxic": is_toxic,
            "categories": toxic_categories
        }

    except Exception as e:
        logger.error(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))