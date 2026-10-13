"""Script: "Figma Auto Layout in 10 Minutes" (Hinglish long video, target 6-8 min).

Each line: (visual_key, spoken_devanagari_for_tts, caption_roman_hinglish)
visual_key tells the renderer what to animate on the Figma-style canvas.
"""

TITLE = "Figma Auto Layout in 10 Minutes (Hindi) | Card, Spacing, Resizing + Common Mistakes"

CHAPTERS = [
    ("00:00", "Hook"),
    ("hook_end", "Auto Layout kya hai?"),
    ("build", "Card banana shuru karo"),
    ("spacing", "Gap aur Padding"),
    ("align", "Alignment"),
    ("nest", "Nested Auto Layout (Button)"),
    ("resize", "Resizing: Hug, Fixed, Fill"),
    ("mistakes", "5 Common Mistakes"),
    ("recap", "Recap"),
]

SCRIPT = [
    # ---------------- HOOK
    ("hook_broken_card",
     "अगर आपके फिग्मा डिज़ाइन में टेक्स्ट बदलते ही सब कुछ टूट जाता है, तो ये वीडियो आपके लिए है।",
     "Text badalte hi design TOOT jaata hai? Ye video aapke liye hai."),
    ("hook_fixed_card",
     "आज सिर्फ दस मिनट में ऑटो लेआउट सीखेंगे। एक रियल प्रोडक्ट कार्ड बनाएंगे, स्पेसिंग, रीसाइज़िंग, और वो गलतियाँ जो नब्बे परसेंट बिगिनर्स करते हैं।",
     "Aaj 10 minute mein AUTO LAYOUT. Real card, spacing, resizing aur 90% beginners wali galtiyan."),
    ("hook_chapters",
     "तो चलिए, शुरू करते हैं।",
     "Chaliye, shuru karte hain!"),

    # ---------------- WHAT IS AUTO LAYOUT
    ("what_manual",
     "पहले समझते हैं कि प्रॉब्लम क्या है। ये कार्ड मैंने हाथ से बनाया है। हर एलिमेंट को खींच खींच कर जगह पर रखा है।",
     "Pehle problem samjho. Ye card maine HAATH se banaya hai."),
    ("what_manual_break",
     "अब अगर मैं टाइटल को थोड़ा लंबा कर दूँ, तो देखो, टेक्स्ट नीचे वाले एलिमेंट के ऊपर चढ़ गया। अब हर चीज़ को फिर से हिलाना पड़ेगा।",
     "Title lamba kiya, aur text OVERLAP ho gaya. Ab sab dobara hilao."),
    ("what_definition",
     "ऑटो लेआउट यही काम अपने आप करता है। ये फिग्मा को बताता है कि चीज़ें किस डायरेक्शन में लगेंगी, उनके बीच कितना स्पेस होगा, और साइज़ बदलने पर क्या होगा।",
     "Auto Layout batata hai: DIRECTION, SPACE, aur RESIZE pe kya hoga."),
    ("what_css",
     "अगर आपने कभी सी एस एस फ्लेक्सबॉक्स यूज़ किया है, तो ये बिल्कुल वैसा ही है। और अगर नहीं किया, तो कोई बात नहीं, आज समझ जाओगे।",
     "CSS Flexbox jaisa hi hai. Nahi pata? Koi baat nahi."),

    # ---------------- BUILD
    ("build_elements",
     "चलो कार्ड बनाते हैं। मेरे पास चार चीज़ें हैं। एक इमेज, एक टाइटल, एक डिस्क्रिप्शन और प्राइस, और एक बटन।",
     "Card ke 4 parts: IMAGE, TITLE, DETAILS, BUTTON."),
    ("build_select",
     "सबसे पहले इन चारों को सेलेक्ट करो। ध्यान रखना, इन्हें ऊपर से नीचे उसी ऑर्डर में रखो जैसा आपको चाहिए।",
     "Charon ko SELECT karo. Order upar se neeche sahi rakho."),
    ("build_shift_a",
     "अब कीबोर्ड पर शिफ्ट प्लस ए दबाओ। बस। फिग्मा ने इन सबके चारों ओर एक ऑटो लेआउट फ्रेम बना दिया।",
     "Ab dabao SHIFT + A. Bas! Auto Layout frame ban gaya."),
    ("build_layers",
     "लेयर्स पैनल में देखो, फ्रेम के आइकन पर ये लाइनें दिख रही हैं। इसका मतलब ये ऑटो लेआउट फ्रेम है। इसका नाम प्रोडक्ट कार्ड रख देते हैं।",
     "Layers mein naya ICON dikha. Naam rakho: Product Card."),
    ("build_direction",
     "राइट साइड में ऑटो लेआउट सेक्शन आ गया। पहला ऑप्शन है डायरेक्शन। नीचे वाला ऐरो मतलब वर्टिकल, सब चीज़ें ऊपर से नीचे। साइड वाला ऐरो मतलब हॉरिज़ॉन्टल।",
     "Pehla option DIRECTION. Neeche arrow = Vertical, side arrow = Horizontal."),
    ("build_direction_demo",
     "देखो, हॉरिज़ॉन्टल करते ही सब एक लाइन में आ गए। हमें कार्ड चाहिए, तो वापस वर्टिकल कर देते हैं।",
     "Horizontal kiya, sab ek line mein. Card ke liye wapas VERTICAL."),

    # ---------------- SPACING
    ("gap_intro",
     "अब आता है सबसे काम का फीचर, गैप। गैप मतलब हर एलिमेंट के बीच का स्पेस।",
     "Sabse kaam ka feature: GAP. Items ke beech ka space."),
    ("gap_change",
     "मैं गैप को आठ से सोलह कर देता हूँ। देखो, हर एलिमेंट के बीच बराबर स्पेस अपने आप आ गया। अब कुछ भी हाथ से हिलाने की ज़रूरत नहीं।",
     "Gap 8 se 16 kiya. Har jagah EQUAL space, apne aap."),
    ("gap_tip",
     "एक टिप, स्पेसिंग हमेशा चार या आठ के मल्टीपल में रखो, जैसे आठ, बारह, सोलह, चौबीस। इससे डिज़ाइन साफ और कंसिस्टेंट लगता है।",
     "TIP: spacing 4 ya 8 ke multiple mein rakho: 8, 12, 16, 24."),
    ("gap_auto",
     "गैप में एक ऑटो ऑप्शन भी है। इससे चीज़ें फ्रेम में बराबर फैल जाती हैं। इसे स्पेस बिटवीन कहते हैं। ये नेवबार जैसी चीज़ों में काम आता है।",
     "Gap = AUTO matlab Space Between. Navbar mein kaam aata hai."),
    ("pad_intro",
     "अब पैडिंग। पैडिंग मतलब फ्रेम के किनारे और कंटेंट के बीच का स्पेस। गैप अंदर के बीच का स्पेस है, पैडिंग बाहर का।",
     "PADDING = frame ke kinaare aur content ke beech ka space."),
    ("pad_change",
     "पैडिंग चौबीस कर देते हैं। कार्ड अब साँस ले रहा है।",
     "Padding 24. Ab card SAANS le raha hai."),
    ("pad_individual",
     "अगर हर साइड पर अलग पैडिंग चाहिए, तो इस आइकन पर क्लिक करो। अब ऊपर, नीचे, लेफ्ट, राइट अलग अलग सेट कर सकते हो।",
     "Har side alag padding chahiye? Is ICON pe click karo."),

    # ---------------- ALIGN
    ("align_intro",
     "अगला है अलाइनमेंट। ये छोटा सा ग्रिड बताता है कि चीज़ें फ्रेम के अंदर कहाँ बैठेंगी।",
     "ALIGNMENT grid batata hai items kahan baithenge."),
    ("align_demo",
     "टॉप लेफ्ट पर सब लेफ्ट में। सेंटर पर क्लिक करो तो सब बीच में आ गया। कार्ड के लिए मैं टॉप लेफ्ट ही रखूँगा।",
     "Top-left, Center... card ke liye TOP-LEFT best."),

    # ---------------- NESTED
    ("nest_intro",
     "अब असली जादू, नेस्टेड ऑटो लेआउट। मतलब ऑटो लेआउट के अंदर एक और ऑटो लेआउट।",
     "Asli jaadu: NESTED Auto Layout. Andar ek aur Auto Layout."),
    ("nest_button",
     "ये बटन देखो। टेक्स्ट को सेलेक्ट करो, शिफ्ट प्लस ए दबाओ, और फ्रेम को ब्लू कलर दो। डायरेक्शन हॉरिज़ॉन्टल, पैडिंग लेफ्ट राइट चौबीस, ऊपर नीचे बारह।",
     "Button: text pe SHIFT + A. Padding 24 side, 12 upar-neeche."),
    ("nest_button_grow",
     "अब बटन का टेक्स्ट बदलो, ऐड टू कार्ट से बाय नाउ विद फ्री डिलीवरी। बटन अपने आप बड़ा हो गया। कोई रीसाइज़ नहीं करना पड़ा।",
     "Text badla, button APNE AAP bada ho gaya!"),
    ("nest_details",
     "इसी तरह डिस्क्रिप्शन और प्राइस को भी एक छोटे ऑटो लेआउट में डाल दो, गैप चार। अब कार्ड के अंदर तीन लेवल का स्ट्रक्चर है।",
     "Description + Price ko bhi group karo. Gap 4."),

    # ---------------- RESIZE
    ("resize_intro",
     "अब सबसे ज़रूरी टॉपिक, रीसाइज़िंग। ज़्यादातर लोग यहीं कन्फ्यूज़ होते हैं। इसके तीन ऑप्शन हैं। हग कंटेंट्स, फिक्स्ड, और फिल कंटेनर।",
     "Sabse zaroori: RESIZING. 3 options: HUG, FIXED, FILL."),
    ("resize_hug",
     "हग कंटेंट्स मतलब फ्रेम अपने कंटेंट जितना ही बड़ा होगा। कंटेंट बढ़ा, फ्रेम बढ़ा। बटन ने यही किया था।",
     "HUG = frame utna hi bada jitna content."),
    ("resize_fixed",
     "फिक्स्ड मतलब साइज़ लॉक। मैं कार्ड की विड्थ फिक्स्ड तीन सौ बीस कर देता हूँ। अब कार्ड इससे चौड़ा नहीं होगा।",
     "FIXED = size LOCK. Card width fixed 320."),
    ("resize_fill",
     "फिल कंटेनर मतलब अंदर वाली चीज़ पैरेंट की पूरी जगह ले लेगी। बटन को फिल कंटेनर करो, देखो, वो पूरे कार्ड जितना चौड़ा हो गया।",
     "FILL = parent ki poori jagah le lo. Button ab FULL width."),
    ("resize_demo",
     "अब असली टेस्ट। कार्ड की विड्थ खींच कर बदलो। इमेज, टेक्स्ट और बटन, सब साथ में एडजस्ट हो रहे हैं। यही है रिस्पॉन्सिव डिज़ाइन।",
     "Card kheecho, sab saath mein ADJUST. Yahi hai responsive design!"),
    ("resize_text",
     "और अब टाइटल को लंबा करते हैं। टेक्स्ट अगली लाइन में गया, और कार्ड नीचे की तरफ बढ़ गया। कुछ भी ओवरलैप नहीं हुआ। शुरू वाली प्रॉब्लम सॉल्व।",
     "Title lamba kiya, card neeche BADHA. Overlap zero. Problem SOLVED."),
    ("resize_rule",
     "याद रखने का आसान रूल, पैरेंट कार्ड की विड्थ फिक्स्ड, हाइट हग। और अंदर के एलिमेंट्स की विड्थ फिल।",
     "RULE: Card width Fixed, height Hug. Andar wale Fill."),

    # ---------------- MISTAKES
    ("mistakes_intro",
     "अब बात करते हैं उन पाँच गलतियों की, जो लगभग हर बिगिनर करता है।",
     "Ab 5 GALTIYAN jo har beginner karta hai."),
    ("mistake1",
     "गलती नंबर एक, कार्ड की हाइट फिक्स्ड रखना। टेक्स्ट बढ़ा तो कंटेंट कार्ड से बाहर निकल गया या कट गया। हाइट हमेशा हग रखो।",
     "Galti #1: Height FIXED. Content kat gaya. Height = HUG."),
    ("mistake2",
     "गलती नंबर दो, अंदर के एलिमेंट्स को फिक्स्ड छोड़ देना। कार्ड चौड़ा किया, पर बटन वहीं का वहीं। इन्हें फिल कंटेनर करो।",
     "Galti #2: Button FIXED chhoda. Card bada, button nahi. Use FILL."),
    ("mistake3",
     "गलती नंबर तीन, स्पेस के लिए खाली रेक्टैंगल रखना। ये पुराना तरीका है। गैप और पैडिंग यूज़ करो, एक नंबर बदलो और सब अपडेट।",
     "Galti #3: Space ke liye khaali RECTANGLE. Gap use karo."),
    ("mistake4",
     "गलती नंबर चार, लेयर्स के नाम न रखना। फ्रेम एक, फ्रेम दो, फ्रेम तीन। बाद में कुछ समझ नहीं आता। हर ऑटो लेआउट का साफ नाम रखो।",
     "Galti #4: Frame 1, Frame 2, Frame 3... Naam rakho!"),
    ("mistake5",
     "गलती नंबर पाँच, बिना ज़रूरत बहुत ज़्यादा नेस्टिंग करना। हर छोटी चीज़ को अलग फ्रेम में मत डालो। जितना ज़रूरी हो, उतना ही नेस्ट करो।",
     "Galti #5: Bahut zyada NESTING. Sirf zaroorat jitna."),

    # ---------------- RECAP
    ("recap",
     "जल्दी से रिकैप। शिफ्ट प्लस ए से ऑटो लेआउट। डायरेक्शन, गैप, पैडिंग, अलाइनमेंट। नेस्टिंग से बटन जैसे कंपोनेंट्स। और रीसाइज़िंग में हग, फिक्स्ड, फिल।",
     "RECAP: Shift+A, Gap, Padding, Align, Nesting, Hug-Fixed-Fill."),
    ("cta",
     "अब खुद ट्राई करो और अपना कार्ड बनाओ। अगर वीडियो काम का लगा, तो लाइक करो, सब्सक्राइब करो, और कमेंट में बताओ अगला फिग्मा टॉपिक कौन सा चाहिए। मिलते हैं अगली वीडियो में।",
     "Khud TRY karo! Like, Subscribe, aur comment karo next topic."),
]

# Short-form cuts (vertical 1080x1920) built from the same scenes.
SHORTS = {
    "short1_shift_a": ["what_manual_break", "build_shift_a", "gap_change", "resize_text"],
    "short2_hug_fixed_fill": ["resize_intro", "resize_hug", "resize_fixed", "resize_fill", "resize_rule"],
    "short3_mistakes_1_2_3": ["mistakes_intro", "mistake1", "mistake2", "mistake3"],
    "short4_button_trick": ["nest_button", "nest_button_grow", "resize_fill"],
}
