from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
# from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, request, jsonify
# import spacy

# spacy.load('en_core_web_sm')
from chatterbot import languages
languages.ENG.ISO_639_1 = "en_core_web_sm"

chatbot = ChatBot('WISO', storage_adapter = 'chatterbot.storage.SQLStorageAdapter', 
        logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response':     "Hi!👋 I am WISO. How can I help you today? <br><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>About Suryadatta</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Courses Offered</span></button></div><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/admission_icon.png' alt='Image'><span>Admission Details</span></button></div><br> <div class='container'><button class='image-button' id='button_ext' ><img src='styles/images/applu_icon.png' alt='Image'><span>Placements</span></button></div><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/student_icon.png' alt='Image'><span>Student Life</span></button></div><br><div class=container'><button class='image-button' id='button_ext'><img src='styles/images/events_icon.png' alt='Image'><span>Events</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/contact_icon.png' alt='Image'><span>Contact Details</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Apply Online</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Book Appointment</span></button></div>",
            'maximum_similarity_threshold': 0.90
        }
        ],
        database_uri='sqlite:///database.sqlite3')



conversation = [
    "hi",
    "hello",
    "Hi!👋 I am WISO. How can I help you today? <br><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>About Suryadatta</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Courses Offered</span></button></div><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/admission_icon.png' alt='Image'><span>Admission Details</span></button></div><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/applu_icon.png' alt='Image'><span>Placements</span></button></div><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/student_icon.png' alt='Image'><span>Student Life</span></button></div><br><div class=container'><button class='image-button' id='button_ext'><img src='styles/images/events_icon.png' alt='Image'><span>Events</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/contact_icon.png' alt='Image'><span>Contact Details</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Apply Online</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Book Appointment</span></button></div>",
    "About Suryadatta", 
    "The Suryadatta Education Foundation (SEF) is a Charitable Trust registered under the Bombay Public Trust Act 1950. It is a Jain Minority self-financed Institution. Professor Dr. Sanjay B. Chordiya, with the blessings of his parents, Late Smt Ratanbai Chordiya & Late Shri Bansilalji Chordiya, established Suryadatta Education Foundation in the year 1999 in Pune, popularly known as Oxford of the East. <br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>" ,
    "Courses Offered",
    "<br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>CBSE School</span></button></div> <br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Courses for X pass</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Courses for XII pass</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Courses for graduates</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Doctoral Research</span></button></div>",
    "CBSE School",
    "Suryadatta National School (SNS) in Pune is a leading educational institution offering a comprehensive range of education from Play Group to CBSE-affiliated classes, spanning 1st to 12th standard. Since its establishment on December 12, 2012, Suryadatta National School has garnered numerous accolades and distinctions.<br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Courses for X pass",
    "<ul><li>Junior College</li><li>Interior Design</li><li>Fashion Design</li><li>Health Science</li><li>Teachers Training</li><li>Computer Animation</li><li>Hotel Management & Travel Tourism</li><li>Event Management</li><li>Foreign Languages</li><li>Physical Education And Fitness</li> <li>Beauty & Wellness</li><li>Journalism / Library & Information Science</li></ul> <br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Courses for XII pass",
    "<ul><li>Arts</li><li>Commerce & Management</li><li>Information Technology</li><li>Animation</li><li>Hotel Management & Travel Tourism</li><li>Fashion Design</li><li>Interior Design</li><li>Physiotherapy</li><li>Pharmacy</li><li>Event Management</li><li>Law</li><li>Theatre & Performing Arts</li><li>Yoga & Naturopathy</li></ul><br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Courses for graduates",
    "Master of Business Administration (MBA), Post Graduate Diploma in Management (PGDM), Master of Computer Application (MCA), Master of Commerce, M.A. Psychology, M.A. Journalism & Mass Communication, M.Sc. Media & Communication Studies, M.Sc. Computer Science, M.Sc. Computer Science (Data Science), M.Sc. Statistics, M.Sc. Computer Application, M.Sc Mathematics, M.Sc. H.S. (Hospitality Studies), Post Graduate Diploma in Foreign Trade (PGDFT), Post Graduate Diploma in Financial Services (PGDFS), Post Graduate Diploma in Marketing Management (PGDMM), Post Graduate Diploma in International Business (PGDIB), Post Graduate Diploma in Material & Logistics Management (PGDMLM)<br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Doctoral Research",
    "Suryadatta Group of Institutes, Pune has established two, Savitribai Phule Pune University recognized, doctoral research centers in management to promote research for developing management frameworks rooted in Indian realities. <br>For Management Research : visit www.simmc.org / www.sibmt.org . <br>Research centres in the area of Hospitality Management, Commerce are also available.<br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Admission Details",
    "<br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Detail Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Admission Process</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Download Admission Form and Brochure</span></button></div>",
    "Detail Enquiry Form",
    "<br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>School Enquiry Form</span></button></div> <br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Juinor College Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Bachelor Degree Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Master Degree Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Certificates, Diploma and PG Courses and other courses Enquiry Form.</span></button></div> <br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>BA LLB Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>D Pharm Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>B Pharm Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>BPTh Enquiry Form</span></button></div>" ,
    "School Enquiry Form",
    "<a href='https://www.suryadatta.org/school-admission-form'>School Enquiry Form</a>",
    "Junior College Enquiry Form",
    "<a href='https://www.suryadatta.org/junior-college-admission-form'>Junior College Enquiry Form</a>",
    "Bachelor Degree Enquiry Form",
    "<a href='https://www.suryadatta.org/bachelors-degree-admission-form'>Bachelors Degree Form</a>",
    "Master Degree Enquiry Form",
    "<a href='https://www.suryadatta.org/masters-degree-admission-form'>Masters Degree Form</a>",
    "Certificates, Diploma, PG Courses & Other Courses Enquiry Form",
    "<a href='https://www.suryadatta.org/other-courses-admission-form'>Certificates, Diploma, PG Courses & Other Courses Enquiry Form</a>",
    "BA LLB Enquiry Form",
    "<a href='https://www.suryadatta.org/ba-llb-from'>BA LLB Enquiry Form</a>",
    "D Pharm Enquiry Form",
    "<a href='https://www.suryadatta.org/d-pharm-form'>D Pharm Enquiry Form</a>",
    "B Pharm Enquiry Form",
    "<a href='https://www.suryadatta.org/b-pharm-form'>B Pharm Enquiry Form</a>",
    "BPTh Enquiry Form",
    "<a href='https://www.suryadatta.org/bpth-form'>BPTh Enquiry Form</a>",
    "Admission Process",
    "Fill up the online admission form of respective course / institute (https://www.suryadatta.org/admissions/download-admission-form-and-brochures). Submit all the requisite documents by email on admission@suryadatta.edu.in Our Admission counsellors will revert back with complete information of the admission process w.r.t the course you are interested ASAP. Admission Counselling @ Pune Campus: Monday to Friday. Timing: 11 am to 5 pm @ Pan India: Please connect with our Counsellors on call 8956943821 / 8956932418 / 7262011336 / 8956932404/ 9763266829 For Career Guidance SMS your Name Course & City 8956932400 or Give a missed call on @ 7776072000 / 8956932404. Our Core team member will call back.<br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Download Admission Form and Brochure",
    "Download Link:<br> <a href='https://www.suryadatta.org/admissions/download-admission-form-and-brochures'>Admission Form and Brochure</a>" ,
    "Placements",
    "<br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Suryadatta Institute of Management & Mass Communication (SIMMC)</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Suryadatta Institute of Business Management & Technology (SIBMT)</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Suryadatta College of Hospitality Management & Travel Tourism (SCHMTT)</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Suryadatta College of Management Information Research & Technology (SCMIRT)</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Suryadatta Institute of Fashion Technology (SIFT)</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Suryadatta Institute of Design (SIVAS)</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Pune Institute of Applied Technology (PIAT)</span></button></div>",
    "SIMMC Placements",
    "https://www.suryadatta.org/placements/suryadatta-institute-of-management-mass-communication-simmc",
    "SIBMT Placements",
    "https://www.suryadatta.org/placements/suryadatta-institute-of-business-management-technology-sibmt",
    "SCHMTT Placements",
    "https://www.suryadatta.org/placements/suryadatta-college-of-hospitality-management-travel-tourism-schmtt",
    "SCMIRT Placements",
    "https://www.suryadatta.org/placements/suryadatta-college-of-management-information-research-technology-scmirt",
    "SIFT Placements",
    "https://www.suryadatta.org/placements/suryadatta-institute-of-fashion-design-sift",
    "SIVAS Placements",
    "https://www.suryadatta.org/placements/suryadatta-institute-of-vocational-advanced-studies-sivas",
    "PIAT Placements",
    "https://www.suryadatta.org/placements/pune-institute-of-applied-technology-piat",
    "Student Life",
    "<br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Infrastructure</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Rules & Regulations</span></button></div>",
    "Infrastructure",
    "Campus comprises of: <ul> <li>Class Rooms with modern teaching aids installed in each of the Classroom Tutorial Rooms for Mentoring, Student's Activities, Presentations etc</li><li>Computer / Internet Labs Mobile Lab / Ads Lab Knowledge Resource Center with rich collection of self learning tools such as DVD's, e-journals, Annual Reports etc</li><li>Seminar halls / Conference Hall / Auditorium / Amphitheatre with latest Audio visual facilities Incubation Center Entrepreneurship Cell / Research Center</li><li>Other facilities such as Indoor and Outdoor Games, Gym, Cafeteria, Conference Hall, Seminar Hall, Yoga & Meditation Hall etc</li></ul> <br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Rules & Regulations",
    "For Rules and Regulation, click on the link given below:<br> <a href='https://www.suryadatta.org/other-pages/rules-and-regulations'>Rules and Regulations</a>",
    "Events",
    "<br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>SPARK Annual Exhibition</span></button></div> <br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>La Classe Annual runway Show</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Indian Celebrities Visited Suryadatta</span></button></div>",
    "SPARK Annual Exhibition",
    "Every year, Suryadatta Institute of Fashion Technology (SIFT) organizes an annual exhibition : <b>SPARK</b> showcasing products prepared by its Fashion Design students on any one particular theme.<br> Suryadatta Institute of Fashion Technology aims at imparting knowledge and practical exposure in the key areas of Fashion in their curriculum of 3 years. <br>Students of SIFT arrange an exhibit of innovative and creative products developed under a theme. The approach behind the exhibition is to enlighten the path for others to follow.<br> Through this exhibition the students are given an equal opportunity to represent their talent and creativity in front of others.<br> The fashion design students their creative minds exhibit their learning journey with all of us.<br><br> This year, to commemorate, 75 years Azadi ka Amrit Mahotsav, the students have organized a unique exhibition of 2100 different handcrafted articles and merchandise made by our students with the use of Khadi fabric through its : <b>11th Spark 2023</b>'<br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "La Classe Annual runway Show",
    "Suryadatta Institute of Fashion Technology (SIFT) organizes <b>La Classe</b> Annual Runway fashion show every year to showcase the talent of its students.<br> Every year a fashion show 'La Classé' is conducted in an exhilarating atmosphere full of glamour and glitter. <br>Dozens of Celebrity Models from the tinsel town of Mumbai show case the apparels designed and stitched by the students of SIFT.<br> A large number of celebrities from the fashion world and film industry enhance the charm of the show with their presence. <br>Every year there is a different theme for designing the apparels and students complete a thorough research before creating mind boggling designs. <br><br>The main attraction is the choreography which is created by very well known choreographers like Vishhal Saawaant, Sandeep Dharma and Alesia Raut, an eminent fashion choreographer, fashion stylist and model coordinator in the glamour industry with multiple talents and a perfect blend ot attitude, versatility and experience.<br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Indian Celebrities Visited Suryadatta",
    "Suryadatta Group of Institutes strives for an all round, holistic development of its students who are not only academically excellent but are also versatile and well aware about the newest trends in industry, well equipped with the skills required for exceptional performance at workplaces and ready to lead the ever-evolving global market. This is achieved through robust classroom training coupled with plenty of co-curricular and extra-curricular activities which adds fun in the learning process. One such incredible activity is the <b>'Celebrity Connect for Edutainment'</b>.<br> Celebrities from Bollywood, Marathi Cinema and Performing Arts interact with students at Suryadatta. They share their life stories, struggles, success mantras with students which educates and inspires the students to follow the footsteps of these role models to shine in the world.<br><br> Students enthusiastically participate in these interactions, ask questions to the celebrities about their life, work, experiences, etc. and gain essential knowledge helpful to deal with real world issues.<br><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Main Menu</span></button></div>",
    "Apply Online",
    "<br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>School Enquiry Form</span></button></div> <br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Juinor College Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Bachelor Degree Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Master Degree Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>Certificates, Diploma and PG Courses and other courses Enquiry Form.</span></button></div> <br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>BA LLB Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>D Pharm Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>B Pharm Enquiry Form</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>BPTh Enquiry Form</span></button></div>" ,
    "School Enquiry Form",
    "<a href='https://www.suryadatta.org/school-admission-form'>School Enquiry Form</a>",
    "Junior College Enquiry Form",
    "<a href='https://www.suryadatta.org/junior-college-admission-form'>Junior College Enquiry Form</a>",
    "Bachelors Degree Enquiry Form",
    "<a href='https://www.suryadatta.org/bachelors-degree-admission-form'>Bachelors Degree Form</a>",
    "Masters Degree Enquiry Form",
    "<a href='https://www.suryadatta.org/masters-degree-admission-form'>Masters Degree Form</a>",
    "Certificates, Diploma, PG Courses & Other Courses Enquiry Form",
    "<a href='https://www.suryadatta.org/other-courses-admission-form'>Certificates, Diploma, PG Courses & Other Courses Enquiry Form</a>",
    "BA LLB Enquiry Form",
    "<a href='https://www.suryadatta.org/ba-llb-from'>BA LLB Enquiry Form</a>",
    "D Pharm Enquiry Form",
    "<a href='https://www.suryadatta.org/d-pharm-form'>D Pharm Enquiry Form</a>",
    "B Pharm Enquiry Form",
    "<a href='https://www.suryadatta.org/b-pharm-form'>B Pharm Enquiry Form</a>",
    "BPTh Enquiry Form",
    "<a href='https://www.suryadatta.org/bpth-form'>BPTh Enquiry Form</a>",
    "Contact Details",
    "<b>Call us on:</b> +91 8956360360<br> <br><b>Address:</b> Suryadatta Group of Institutes, Bavdhan, Pune-411 021, Maharashtra, India"
    "Book Appointment",
    '''Please provide the following information to book an appointment<br> 
     <form id="myForm" method="post" action="http://localhost:4000/submit_form">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>
    <br>
    
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
    <br>

    <label for="phone">Phone:</label>
    <input type="tel" id="phone" name="phone" pattern="[0-9]{10}" required>
    <!-- The pattern attribute enforces a 10-digit phone number -->
    <br>

    <label>Choose an option:</label> 
 
    <br>

    <input type="radio" id="slot_1_option" name="choice" value="SLOT_1">
    <label for="slot_1_option">SLOT 1</label>
    <br>

    <input type="radio" id="slot_2_option" name="choice" value="SLOT_2">
    <label for="slot_2_option">SLOT 2</label>
    <br>

    <input type="submit" value="Submit">
</form>


<div id="result"></div>
''',
"Main Menu",
"Hi!👋 I am WISO. How can I help you today? <br><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/about_icon.png' alt='Image'><span>About Suryadatta</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/book_icon.png' alt='Image'><span>Courses Offered</span></button></div><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/admission_icon.png' alt='Image'><span>Admission Details</span></button></div><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/applu_icon.png' alt='Image'><span>Placements</span></button></div><br> <div class='container'><button class='image-button' id='button_ext'><img src='styles/images/student_icon.png' alt='Image'><span>Student Life</span></button></div><br><div class=container'><button class='image-button' id='button_ext'><img src='styles/images/events_icon.png' alt='Image'><span>Events</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/contact_icon.png' alt='Image'><span>Contact Details</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Apply Online</span></button></div><br><div class='container'><button class='image-button' id='button_ext'><img src='styles/images/online_icon.png' alt='Image'><span>Book Appointment</span></button></div>",
"bye",
"Bye!👋 See you again!",
"thank you",
"You are Welcome!👋",
"thanks",
"You are Welcome!👋"
]

# trainer = ListTrainer(chatbot)
# trainer.train(conversation)

list_trainer = ListTrainer(chatbot)
# corpus_trainer = ChatterBotCorpusTrainer(chatbot)

list_trainer.train(conversation)
# corpus_trainer.train('chatterbot.corpus.english.greetings')

from flask_cors import CORS


app = Flask(__name__)

CORS(app)

@app.route("/get_response", methods=['POST'])
def get_bot_response():
    print(request.json)
    try:
        data = request.json
        user_input = data.get('user_input', '')

        response = str(chatbot.get_response(user_input))
        print(response)
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run()
