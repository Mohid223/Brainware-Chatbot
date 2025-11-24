from flask import Flask, render_template, request, jsonify, url_for
import random
import re
from datetime import datetime

app = Flask(__name__)

class BrainwareChatbot:
    def __init__(self):
        self.university_data = self.get_university_data()
        self.programs_data = self.get_complete_programs_data()
        self.setup_keywords()
        
    def get_university_data(self):
        return {
            "university_name": "Brainware University",
            "flickr_gallery": "https://www.flickr.com/photos/brainwareindia/albums/with/72177720329659464",
            "contacts": {
                "website": "https://www.brainwareuniversity.ac.in",
                "admission_email": "admission@brainwareuniversity.ac.in",
                "admission_phone": "+91 70031 62601",
                "general_email": "info@brainwareuniversity.ac.in", 
                "general_phone": "+91 70031 62601"
            },
            "campus": {
                "barasat": "398, Ramkrishnapur Road, Barasat, Near Jagadighata Market, Kolkata, West Bengal 700125",
                "saltlake": "Y8, EP Block, Sector V, Bidhannagar, Kolkata, West Bengal 700091",
                "maps_link": "https://maps.google.com/?q=Brainware+University+Kolkata"
            },
            "reservation_policy": "Reservation policies of Department of Higher Education, West Bengal will be followed. 5% relaxation in marks for reserved category candidates (Except programmes under School of Law)"
        }

    def setup_keywords(self):
        self.keyword_mapping = {
            'engineering': ['engineering', 'btech', 'computer science', 'cse', 'ai', 'machine learning', 'data science', 'cyber security', 'electronics', 'electrical', 'mechanical', 'civil', 'robotics', 'automation'],
            'management': ['management', 'mba', 'bba', 'business', 'business analytics', 'digital marketing', 'hospital management'],
            'commerce': ['commerce', 'bcom', 'accounts', 'finance', 'banking'],
            'law': ['law', 'llb', 'ballb', 'bballb', 'legal'],
            'medical': ['medical', 'nursing', 'pharmacy', 'bsc nursing', 'b.pharm', 'physiotherapy', 'optometry', 'medical lab', 'radiology', 'operation theatre', 'critical care'],
            'biotech': ['biotechnology', 'biosciences', 'biotech'],
            'agriculture': ['agriculture', 'bsc agriculture'],
            'media': ['media', 'journalism', 'animation', 'multimedia', 'film'],
            'humanities': ['humanities', 'english', 'psychology', 'arts'],
            'sciences': ['science', 'bca', 'cyber science', 'computational', 'networking'],
            'fees': ['fee', 'fees', 'cost', 'tuition', 'price', 'charges'],
            'eligibility': ['eligibility', 'criteria', 'qualification', 'required', 'marks'],
            'admission': ['admission', 'apply', 'admit', 'how to join', 'application'],
            'contact': ['contact', 'email', 'phone', 'call', 'number', 'address'],
            'campus': ['campus', 'location', 'map', 'address', 'where', 'hostel'],
            'gallery': ['gallery', 'photo', 'picture', 'flickr', 'campus photo']
        }

    def get_complete_programs_data(self):
        return {
            "engineering": {
                "Computer Science & Engineering": [
                    {"name": "B.Tech in Computer Science & Engineering", "duration": "4 years", "fees": "₹5,49,600", "eligibility": "50% in 10+2 with Physics & Mathematics"},
                    {"name": "B.Tech in CSE (Lateral Entry)", "duration": "3 years", "fees": "₹2,41,200", "eligibility": "45% in relevant Diploma/BSc/BCA"}
                ],
                "Computer Science & Engineering - AI & ML": [
                    {"name": "B.Tech in CSE - AI & Machine Learning", "duration": "4 years", "fees": "₹5,49,600", "eligibility": "50% in 10+2 with Physics & Mathematics"},
                    {"name": "B.Tech in CSE - AI & ML (LE)", "duration": "3 years", "fees": "₹2,41,200", "eligibility": "45% in relevant Diploma/BSc/BCA"}
                ],
                "Computer Science & Engineering - Data Science": [
                    {"name": "B.Tech in CSE - Data Science", "duration": "4 years", "fees": "₹5,49,600", "eligibility": "50% in 10+2 with Physics & Mathematics"},
                    {"name": "B.Tech in CSE - Data Science (LE)", "duration": "3 years", "fees": "₹2,41,200", "eligibility": "45% in relevant Diploma/BSc/BCA"}
                ],
                "Computer Science & Engineering - Cyber Security": [
                    {"name": "B.Tech in CSE - Cyber Security", "duration": "4 years", "fees": "₹5,49,600", "eligibility": "50% in 10+2 with Physics & Mathematics"},
                    {"name": "B.Tech in CSE - Cyber Security (LE)", "duration": "3 years", "fees": "₹2,41,200", "eligibility": "45% in relevant Diploma/BSc/BCA"}
                ],
                "Electronics & Communication Engineering": [
                    {"name": "B.Tech in Robotics & Automation (LE)", "duration": "3 years", "fees": "₹2,41,200", "eligibility": "45% in relevant Diploma/BSc"}
                ],
                "Electrical Engineering": [
                    {"name": "B.Tech in Electrical Engineering (LE)", "duration": "3 years", "fees": "₹2,16,200", "eligibility": "45% in relevant Diploma/BSc"}
                ],
                "Mechanical Engineering": [
                    {"name": "B.Tech in Mechanical Engineering (LE)", "duration": "3 years", "fees": "₹2,16,200", "eligibility": "45% in relevant Diploma/BSc"}
                ],
                "Biotechnology": [
                    {"name": "B.Tech in Biotechnology", "duration": "4 years", "fees": "₹5,29,600", "eligibility": "50% in 10+2 with Physics & Chemistry"},
                    {"name": "B.Tech in Biotechnology (LE)", "duration": "3 years", "fees": "₹2,41,200", "eligibility": "45% in relevant Diploma/BSc"}
                ]
            },
            "management": {
                "Business Administration": [
                    {"name": "BBA (Honours)", "duration": "4 years", "fees": "₹4,47,600", "eligibility": "50% in 10+2"},
                    {"name": "BBA (Honours) in Business Analytics", "duration": "4 years", "fees": "₹4,77,600", "eligibility": "55% in 10+2"},
                    {"name": "BBA (Honours) in Digital Marketing", "duration": "4 years", "fees": "₹4,47,600", "eligibility": "50% in 10+2"},
                    {"name": "BBA", "duration": "3 years", "fees": "₹3,57,200", "eligibility": "50% in 10+2"}
                ],
                "Hospital Management": [
                    {"name": "BBA (Honours) in Hospital Management", "duration": "4 years", "fees": "₹4,91,600", "eligibility": "50% in 10+2"},
                    {"name": "BBA in Hospital Management", "duration": "3 years", "fees": "₹3,82,200", "eligibility": "50% in 10+2"}
                ]
            },
            "commerce": {
                "Commerce": [
                    {"name": "B.Com (Honours) in Accounts, Finance & Banking", "duration": "4 years", "fees": "₹2,72,600", "eligibility": "50% in 10+2 (Commerce/Science)"},
                    {"name": "B.Com in Accounts, Finance & Banking", "duration": "3 years", "fees": "₹2,29,200", "eligibility": "50% in 10+2 (Commerce/Science)"}
                ]
            },
            "law": {
                "Law": [
                    {"name": "Bachelor of Law (LLB)", "duration": "3 years", "fees": "₹3,30,200", "eligibility": "45% in Graduation"},
                    {"name": "BBA & Bachelor of Law (BBA LLB)", "duration": "5 years", "fees": "₹5,47,000", "eligibility": "50% in 10+2"},
                    {"name": "BA & Bachelor of Law (BA LLB)", "duration": "5 years", "fees": "₹5,47,000", "eligibility": "50% in 10+2"}
                ]
            },
            "medical": {
                "Pharmacy": [
                    {"name": "Bachelor of Pharmacy", "duration": "4 years", "fees": "₹6,99,600", "eligibility": "60% in 10+2 with PCB/PCM"},
                    {"name": "B.Pharmacy (Lateral Entry)", "duration": "3 years", "fees": "₹4,76,200", "eligibility": "45% in D.Pharm"}
                ],
                "Nursing": [
                    {"name": "B.Sc in Nursing", "duration": "4 years", "fees": "₹6,90,000", "eligibility": "45% in 10+2 with PCB (Female only)"}
                ],
                "Allied Health Sciences": [
                    {"name": "B.Sc in Medical Lab Technology", "duration": "3.5 years", "fees": "₹3,99,200", "eligibility": "60% in 10+2 with PCB"},
                    {"name": "B.Sc in Physiotherapy", "duration": "4.5 years", "fees": "₹3,99,200", "eligibility": "60% in 10+2 with PCB"},
                    {"name": "Bachelor of Optometry", "duration": "4 years", "fees": "₹3,99,200", "eligibility": "60% in 10+2 with PCB"}
                ]
            },
            "sciences": {
                "Computer Applications": [
                    {"name": "BCA (Honours)", "duration": "4 years", "fees": "₹4,72,600", "eligibility": "50% in 10+2"},
                    {"name": "BCA (Honours) in Mobile App & Web Tech", "duration": "4 years", "fees": "₹4,97,600", "eligibility": "50% in 10+2"},
                    {"name": "BCA", "duration": "3 years", "fees": "₹3,69,200", "eligibility": "50% in 10+2"}
                ],
                "Cyber Security": [
                    {"name": "B.Sc (Honours) in Advanced Networking & Cyber Security", "duration": "4 years", "fees": "₹3,92,600", "eligibility": "50% in 10+2"},
                    {"name": "B.Sc in Advanced Networking & Cyber Security", "duration": "3 years", "fees": "₹3,10,200", "eligibility": "50% in 10+2"}
                ]
            },
            "biotech": {
                "Biotechnology": [
                    {"name": "B.Sc (Honours) in Biotechnology", "duration": "4 years", "fees": "₹4,30,600", "eligibility": "60% in 10+2 with Chemistry & Biology"},
                    {"name": "B.Sc in Biotechnology", "duration": "3 years", "fees": "₹3,45,200", "eligibility": "60% in 10+2 with Chemistry & Biology"}
                ]
            },
            "agriculture": {
                "Agriculture": [
                    {"name": "B.Sc (Honours) in Agriculture", "duration": "4 years", "fees": "₹4,34,600", "eligibility": "60% in 10+2 with PCB/Mathematics"}
                ]
            },
            "media": {
                "Media Science": [
                    {"name": "B.Sc (Honours) in Media Science & Journalism", "duration": "4 years", "fees": "₹3,79,100", "eligibility": "50% in 10+2"},
                    {"name": "B.Sc in Media Science & Journalism", "duration": "3 years", "fees": "₹3,02,200", "eligibility": "50% in 10+2"}
                ],
                "Animation & Multimedia": [
                    {"name": "B.Sc (Honours) in Animation & Multimedia", "duration": "4 years", "fees": "₹4,97,600", "eligibility": "50% in 10+2"},
                    {"name": "B.Sc in Animation & Multimedia", "duration": "3 years", "fees": "₹3,92,200", "eligibility": "50% in 10+2"}
                ]
            },
            "humanities": {
                "English": [
                    {"name": "BA (Honours) in English", "duration": "4 years", "fees": "₹1,97,600", "eligibility": "50% in 10+2"},
                    {"name": "BA in English", "duration": "3 years", "fees": "₹1,65,200", "eligibility": "50% in 10+2"}
                ],
                "Psychology": [
                    {"name": "B.Sc (Honours) in Psychology", "duration": "4 years", "fees": "₹2,74,600", "eligibility": "50% in 10+2"},
                    {"name": "B.Sc in Psychology", "duration": "3 years", "fees": "₹2,30,200", "eligibility": "50% in 10+2"}
                ]
            }
        }

    def find_matching_program(self, user_input):
        """Find specific program based on user input"""
        user_input = user_input.lower()
        
        # Search through all programs
        for category, departments in self.programs_data.items():
            for dept_name, programs in departments.items():
                for program in programs:
                    program_name_lower = program['name'].lower()
                    # Check if any significant word from program name is in user input
                    program_words = set(program_name_lower.split())
                    input_words = set(user_input.split())
                    common_words = program_words.intersection(input_words)
                    
                    if len(common_words) >= 2:  # At least 2 matching words
                        return program, dept_name, category
                        
                    # Check for direct keyword matching
                    keywords = ['cse', 'ai', 'ml', 'data science', 'cyber', 'bba', 'mba', 'bca', 'bsc', 'bcom', 'llb', 'nursing', 'pharmacy']
                    for keyword in keywords:
                        if keyword in user_input and keyword in program_name_lower:
                            return program, dept_name, category
        
        return None, None, None

    def get_program_response(self, program, department, category):
        """Generate detailed response for a specific program"""
        response = f"🎓 **{program['name']}**\n\n"
        response += f"**Department:** {department}\n"
        response += f"**Category:** {category.title()}\n"
        response += f"**Duration:** {program['duration']}\n"
        response += f"**Total Fees:** {program['fees']}\n"
        response += f"**Eligibility:** {program['eligibility']}\n\n"
        response += f"💡 *{self.university_data['reservation_policy']}*"
        
        return response

    def get_category_programs(self, category):
        """Get all programs in a category"""
        if category not in self.programs_data:
            return None
            
        response = f"🎓 **{category.upper()} PROGRAMS**\n\n"
        for department, programs in self.programs_data[category].items():
            response += f"**{department}:**\n"
            for program in programs:
                response += f"• {program['name']}\n"
                response += f"  Duration: {program['duration']} | Fees: {program['fees']}\n"
            response += "\n"
        
        return response

    def get_fee_summary(self):
        """Generate comprehensive fee summary"""
        response = "💰 **COMPREHENSIVE FEE STRUCTURE**\n\n"
        
        fee_categories = {
            "🏛️ ENGINEERING (B.Tech)": "₹5,49,600 (4 years)",
            "💼 MANAGEMENT (BBA)": "₹4,47,600 (4 years)",
            "📊 COMMERCE (B.Com)": "₹2,72,600 (4 years)",
            "⚖️ LAW (BBA LLB)": "₹5,47,000 (5 years)",
            "🏥 MEDICAL & HEALTH": "₹6,90,000 - ₹6,99,600",
            "💻 COMPUTER APPLICATIONS": "₹4,72,600 (4 years)",
            "🔬 BIOTECHNOLOGY": "₹5,29,600 (4 years)",
            "🌾 AGRICULTURE": "₹4,34,600 (4 years)",
            "🎬 MEDIA & ANIMATION": "₹4,97,600 (4 years)",
            "📚 HUMANITIES": "₹1,97,600 (4 years)"
        }
        
        for category, fee in fee_categories.items():
            response += f"{category}: {fee}\n"
        
        response += "\n💡 *Ask about specific program for detailed fees*"
        return response

    def get_eligibility_summary(self):
        """Generate eligibility summary"""
        response = "📋 **ELIGIBILITY CRITERIA SUMMARY**\n\n"
        
        eligibility_rules = {
            "Engineering Programs": "50% in 10+2 with Physics & Mathematics",
            "Management Programs": "50% in 10+2 (any discipline)",
            "Law Programs": "45% in Graduation / 50% in 10+2",
            "Medical Programs": "60% in 10+2 with Physics, Chemistry, Biology",
            "Science Programs": "50% in 10+2 (any discipline)",
            "Commerce Programs": "50% in 10+2 (Commerce/Science)",
            "Arts & Humanities": "50% in 10+2 (any discipline)"
        }
        
        for program, criteria in eligibility_rules.items():
            response += f"• **{program}:** {criteria}\n"
        
        response += f"\n💡 *{self.university_data['reservation_policy']}*"
        return response

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        print(f"Processing: {user_input}")
        
        # First, try to find specific program match
        program, department, category = self.find_matching_program(user_input)
        if program:
            return {
                'text': self.get_program_response(program, department, category),
                'actions': [
                    {'type': 'website', 'label': '🌐 Apply Now', 'value': self.university_data['contacts']['website']},
                    {'type': 'phone', 'label': '📞 Admission Help', 'value': self.university_data['contacts']['admission_phone']}
                ]
            }
        
        # Check category matches
        for category_name, keywords in self.keyword_mapping.items():
            if any(keyword in user_input for keyword in keywords):
                if category_name in ['fees', 'fee']:
                    return {
                        'text': self.get_fee_summary(),
                        'actions': [
                            {'type': 'website', 'label': '🌐 Detailed Fees', 'value': self.university_data['contacts']['website']},
                            {'type': 'phone', 'label': '📞 Fee Inquiry', 'value': self.university_data['contacts']['admission_phone']}
                        ]
                    }
                elif category_name in ['eligibility']:
                    return {
                        'text': self.get_eligibility_summary(),
                        'actions': [
                            {'type': 'website', 'label': '🌐 Full Eligibility', 'value': self.university_data['contacts']['website']}
                        ]
                    }
                elif category_name in self.programs_data:
                    category_response = self.get_category_programs(category_name)
                    if category_response:
                        return {
                            'text': category_response,
                            'actions': [
                                {'type': 'website', 'label': f'🌐 {category_name.title()} Details', 'value': self.university_data['contacts']['website']},
                                {'type': 'email', 'label': '📧 Query', 'value': self.university_data['contacts']['admission_email']}
                            ]
                        }
        
        # Default responses for common queries
        default_responses = {
            'greeting': {
                'text': "Hello! Welcome to Brainware University Assistant! 🎓\n\nI can help you with:\n• Program Details & Fees 💰\n• Eligibility Criteria 📋\n• Admission Process 📝\n• Campus Information 🏢\n• Contact Details 📞\n\nTry asking about specific programs like 'CSE fees', 'BBA eligibility', or 'Law programs'!",
                'actions': []
            },
            'admission': {
                'text': "📝 **ADMISSION PROCESS**\n\n1. **Online Application** - Fill application form\n2. **Entrance Test** - Appear for university test\n3. **Counseling Session** - Personal interview & guidance\n4. **Document Verification** - Submit required documents\n5. **Fee Payment** - Complete admission formalities\n\n⏰ *Apply early for scholarship opportunities!*",
                'actions': [
                    {'type': 'website', 'label': '🌐 Online Application', 'value': self.university_data['contacts']['website']},
                    {'type': 'phone', 'label': '📞 Admission Help', 'value': self.university_data['contacts']['admission_phone']}
                ]
            },
            'contact': {
                'text': f"📞 **CONTACT INFORMATION**\n\n**Admission Office:**\n{self.university_data['contacts']['admission_phone']}\n{self.university_data['contacts']['admission_email']}\n\n**Barasat Campus:**\n{self.university_data['campus']['barasat']}\n\n**Salt Lake Campus:**\n{self.university_data['campus']['saltlake']}",
                'actions': [
                    {'type': 'phone', 'label': '📞 Call Now', 'value': self.university_data['contacts']['admission_phone']},
                    {'type': 'email', 'label': '📧 Email', 'value': self.university_data['contacts']['admission_email']},
                    {'type': 'maps', 'label': '🗺️ Barasat Campus', 'value': self.university_data['campus']['maps_link']},
                    {'type': 'website', 'label': '🌐 Website', 'value': self.university_data['contacts']['website']}
                ]
            },
            'campus': {
                'text': f"🏢 **CAMPUS INFORMATION**\n\n**Main Campus (Barasat):**\n{self.university_data['campus']['barasat']}\n\n**City Campus (Salt Lake):**\n{self.university_data['campus']['saltlake']}\n\n**Facilities:**\n• Modern Classrooms & Smart Boards\n• Advanced Computer Labs & Workshops\n• Central Library with Digital Resources\n• Hostels for Boys & Girls\n• Sports Complex & Gymnasium\n• Cafeteria & Food Court\n• Medical Facilities\n• Transportation Services",
                'actions': [
                    {'type': 'maps', 'label': '🗺️ Barasat Campus', 'value': self.university_data['campus']['maps_link']},
                    {'type': 'gallery', 'label': '📸 Campus Photos', 'value': self.university_data['flickr_gallery']},
                    {'type': 'phone', 'label': '📞 Campus Info', 'value': self.university_data['contacts']['general_phone']}
                ]
            },
            'gallery': {
                'text': "📸 **CAMPUS GALLERY**\n\nExplore our state-of-the-art infrastructure through photos:\n• Modern Academic Blocks\n• Advanced Laboratories\n• Library & Learning Centers\n• Hostel Facilities\n• Sports Complex\n• Student Activities\n• Cultural Events\n• Campus Life",
                'actions': [
                    {'type': 'gallery', 'label': '🖼️ Open Flickr Gallery', 'value': self.university_data['flickr_gallery']}
                ]
            },
            'default': {
                'text': "I'm here to help with Brainware University information! 🎓\n\nTry these queries:\n• 'Engineering programs fees'\n• 'BBA eligibility criteria'\n• 'Law course duration'\n• 'Medical programs'\n• 'Campus facilities'\n• 'Admission process'\n• 'Contact information'\n\nOr ask about specific programs like Computer Science, Business, Law, Medical, etc.!",
                'actions': [
                    {'type': 'website', 'label': '🌐 University Website', 'value': self.university_data['contacts']['website']},
                    {'type': 'phone', 'label': '📞 Call for Help', 'value': self.university_data['contacts']['admission_phone']}
                ]
            }
        }
        
        # Simple keyword matching for default responses
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'namaste']):
            return default_responses['greeting']
        elif any(word in user_input for word in ['admission', 'apply', 'admit']):
            return default_responses['admission']
        elif any(word in user_input for word in ['contact', 'email', 'phone']):
            return default_responses['contact']
        elif any(word in user_input for word in ['campus', 'location', 'hostel']):
            return default_responses['campus']
        elif any(word in user_input for word in ['gallery', 'photo', 'picture']):
            return default_responses['gallery']
        else:
            return default_responses['default']

chatbot = BrainwareChatbot()

@app.route('/')
def home():
    return render_template('index.html', university_data=chatbot.university_data)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        print(f"Received: {user_message}")
        
        bot_response = chatbot.get_response(user_message)
        
        return jsonify({
            'success': True,
            'user_message': user_message,
            'bot_response': bot_response,
            'timestamp': datetime.now().strftime("%H:%M")
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'bot_response': {
                'text': 'Sorry, I encountered an error. Please try again.',
                'actions': []
            }
        }), 500

@app.route('/programs')
def programs_list():
    """API endpoint to get all programs"""
    return jsonify(chatbot.programs_data)

@app.route('/fees')
def fees_summary():
    """API endpoint to get fee summary"""
    return jsonify({'fee_summary': chatbot.get_fee_summary()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)