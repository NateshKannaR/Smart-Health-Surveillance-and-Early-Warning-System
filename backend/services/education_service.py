from typing import Dict, List
import json

class HealthEducationService:
    """Health Education and Awareness Service"""
    
    def __init__(self):
        self.educational_content = self._load_educational_content()
    
    def _load_educational_content(self) -> Dict:
        """Load educational content in multiple languages"""
        return {
            "water_safety": {
                "en": {
                    "title": "Water Safety Guidelines",
                    "content": [
                        "Boil water for at least 1 minute before drinking",
                        "Use water purification tablets if boiling is not possible",
                        "Store treated water in clean, covered containers",
                        "Avoid ice unless made from safe water",
                        "Use bottled water from reliable sources"
                    ],
                    "video_url": "/videos/water_safety_en.mp4"
                },
                "hi": {
                    "title": "पानी की सुरक्षा दिशानिर्देश",
                    "content": [
                        "पीने से पहले पानी को कम से कम 1 मिनट तक उबालें",
                        "यदि उबालना संभव नहीं है तो पानी शुद्धीकरण गोलियों का उपयोग करें",
                        "उपचारित पानी को साफ, ढके हुए कंटेनरों में स्टोर करें"
                    ]
                },
                "as": {
                    "title": "পানীৰ সুৰক্ষা নিৰ্দেশনা",
                    "content": [
                        "খোৱাৰ আগতে পানী কমেও ১ মিনিট উতলাওক",
                        "উতলোৱা সম্ভৱ নহ'লে পানী বিশুদ্ধকৰণ টেবলেট ব্যৱহাৰ কৰক"
                    ]
                }
            },
            "hygiene_practices": {
                "en": {
                    "title": "Personal Hygiene Practices",
                    "content": [
                        "Wash hands frequently with soap and clean water",
                        "Use alcohol-based hand sanitizer when soap is unavailable",
                        "Avoid touching face with unwashed hands",
                        "Cover mouth and nose when coughing or sneezing",
                        "Maintain social distancing during outbreaks"
                    ]
                },
                "hi": {
                    "title": "व्यक्तिगत स्वच्छता प्रथाएं",
                    "content": [
                        "साबुन और साफ पानी से बार-बार हाथ धोएं",
                        "जब साबुन उपलब्ध न हो तो अल्कोहल-आधारित हैंड सैनिटाइज़र का उपयोग करें"
                    ]
                }
            },
            "disease_prevention": {
                "en": {
                    "title": "Disease Prevention",
                    "content": [
                        "Eat freshly cooked, hot food",
                        "Avoid raw or undercooked food",
                        "Peel fruits yourself",
                        "Avoid street vendor food during outbreaks",
                        "Keep food covered and refrigerated when possible"
                    ]
                }
            },
            "emergency_contacts": {
                "en": {
                    "title": "Emergency Contacts",
                    "content": [
                        "District Health Officer: 108",
                        "Local ASHA Worker: Contact your village head",
                        "Ambulance Service: 102",
                        "Water Quality Complaints: 1916"
                    ]
                }
            }
        }
    
    def get_educational_content(self, topic: str, language: str = "en") -> Dict:
        """Get educational content for specific topic and language"""
        if topic not in self.educational_content:
            return {"error": "Topic not found"}
        
        content = self.educational_content[topic]
        if language in content:
            return content[language]
        elif "en" in content:
            return content["en"]  # Fallback to English
        else:
            return {"error": "Content not available"}
    
    def get_all_topics(self, language: str = "en") -> List[Dict]:
        """Get all available educational topics"""
        topics = []
        for topic_key, topic_data in self.educational_content.items():
            if language in topic_data:
                topics.append({
                    "key": topic_key,
                    "title": topic_data[language]["title"],
                    "preview": topic_data[language]["content"][0] if topic_data[language]["content"] else ""
                })
        return topics
    
    def get_awareness_campaign(self, disease: str, language: str = "en") -> Dict:
        """Generate awareness campaign content for specific disease"""
        campaigns = {
            "cholera": {
                "en": {
                    "title": "Cholera Prevention Campaign",
                    "key_messages": [
                        "Drink only boiled or bottled water",
                        "Eat hot, freshly cooked food",
                        "Wash hands frequently",
                        "Seek immediate medical help for severe diarrhea"
                    ],
                    "symptoms": ["Severe watery diarrhea", "Vomiting", "Dehydration", "Muscle cramps"],
                    "prevention": ["Safe water", "Food safety", "Hand hygiene", "Sanitation"]
                },
                "hi": {
                    "title": "हैजा रोकथाम अभियान",
                    "key_messages": [
                        "केवल उबला या बोतलबंद पानी पिएं",
                        "गर्म, ताज़ा पका हुआ खाना खाएं"
                    ]
                }
            },
            "diarrhea": {
                "en": {
                    "title": "Diarrhea Prevention",
                    "key_messages": [
                        "Maintain proper hygiene",
                        "Use ORS for dehydration",
                        "Avoid contaminated water"
                    ]
                }
            }
        }
        
        if disease in campaigns and language in campaigns[disease]:
            return campaigns[disease][language]
        elif disease in campaigns and "en" in campaigns[disease]:
            return campaigns[disease]["en"]
        else:
            return {"error": "Campaign not available"}
    
    def get_tribal_language_content(self, topic: str, tribal_language: str) -> Dict:
        """Get content in tribal languages (placeholder for future implementation)"""
        # This would integrate with local language experts and translators
        return {
            "message": f"Content for {topic} in {tribal_language} is being prepared by local language experts",
            "contact": "Contact your local ASHA worker for verbal translation"
        }