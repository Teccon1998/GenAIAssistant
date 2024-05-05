import json

from langchain_openai import OpenAI
from tools.JobScrape import scrape_linkedin_job
from tools.JSONIFYTool import file_to_json
from tools.LinkedInCurl import scrape_linkedin_profile
from langchain_community.tools.json.tool import JsonSpec
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain.agents import create_json_agent
from langchain.tools import tool
import streamlit as st

@tool
def resumeSuggestion(job_link: str):
    """Input of this tool is a URL link to a linkedIn Job posting. Information found on the job would be compared to 
       a resume and linked json object, and the llm must make suggestions on how to edit the resume to make a better resume. 
       The input is just the job link ex) https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3863706717&eBP=CwEAAAGPRPawW9GhQmyWMk2Js9WJ6bjTpMmJRWHC4BNoAbmJzdV6YcYl165TW27SJOBMJiVthFHWfEWRIfjY1Z7VEEgT6ilFw4ZndjtDeYmMgfaMXLoxSFKch6ZqqGb55G2EY1NtVfixzL8EP1xOet3QNtOC1kCpkuTQ-oU-h5jH758VGFcO22_ptjvYOP18_bGoc3k_YhRNKHVKGY70VR64no9GAzDXovh-v6R1IVLud85UWY2y7gKjwMmh-BLH2gJu_It5usJeJL7A41ZBI1_x1-hgpyp0K_B9xeG8oEm
    """
    # job scrape: JobScrape.py
    #job_info = scrape_linkedin_job(job_link)
    job_info = {
    "apply_url": "https://sg.linkedin.com/jobs/view/externalApply/3257696537?url=https%3A%2F%2Fcareers%2Emicrosoft%2Ecom%2Fus%2Fen%2Fjob%2F1451110%2FContent-Strategist%3Fjobsource%3Dlinkedin%26utm_source%3Dlinkedin%26utm_medium%3Dlinkedin%26utm_campaign%3Dlinkedin-feed\u0026urlHash=I9BQ\u0026trk=public_jobs_apply-link-offsite",
    "company": {
        "logo": "https://media.licdn.com/dms/image/C560BAQE88xCsONDULQ/company-logo_100_100/0/1618231291419?e=2147483647\u0026v=beta\u0026t=rffql7GLHsSqWXKbdP2LJMMv7CMTqu7-Ms9d9tophKI",
        "name": "Microsoft",
        "url": "https://www.linkedin.com/company/microsoft"
    },
    "employment_type": "Full-time",
    "industry": [
        "IT Services and IT Consulting, Computer Hardware Manufacturing, and Software Development"
    ],
    "job_description": "The Global Demand Center (GDC) within the Cloud Marketing group is leading the marketing transformation of Microsoft\u2019s largest and fastest growing commercial businesses. Our always-on integrated marketing programs work to nurture and acquire new customers across segments, targeting business and technical audiences across our commercial cloud portfolio, with programs available in 42 markets and 30 languages. The GDC team is modernizing and integrating these channels through advanced analytics, marketing automation, and digital marketing. We are on a mission to drive market share, consumption, and consistent double-digit+ revenue growth. Content is the fuel that drives the digitally connected customer journeys at the core of the GDC engine, and we\u2019re looking for a skilled, self-motivated, data-driven content strategist to build the content that motivates customers to take action. The Content Strategist will develop and execute content strategies for the ever-critical security space. You will be accountable for understanding the business priorities, getting close to our target audiences, defining the content journeys that attract, nurture, inspire, and retain customers, and manage quality execution and delivery of the content. You will work closely with your counterparts, the integrated marketing strategists, to drive business outcomes. Your network will include product marketers, integrated marketers, relationship marketers, sales, engineering, and agency partners to develop and execute on your plan. Our team: The Lifecycle Programs team is a fast-paced digital marketing organization. We put a focus on getting things done, simplifying anything and everything, and having fun while doing it. We all believe in connecting with customers at scale, supporting them at each stage of the customer journey, from early awareness and consideration, through onboarding and post purchase engagement. You will be in the middle of it all helping to identify the right content that delivers what customers want\u2014where they want it, when they want it, and how they want it.   \n  \n**_Responsibilities  \n_**\n  * Define content journeys for Security and IT professionals across industries.\n  * Build the resulting content strategies designed to accelerate the customer through the lifecycle.\n  * Create a content plan to address the insights in the customer journey and strategy, ensuring the content is aligned to what the customer needs at each stage.\n  * Deliver the content through our internal Studio or with select agency partners.\n  * Be a customer advocate. Relentlessly champion the customer and the experiences they have with the content you create\u2014how they find it, how they consume it, how they use it to make decisions.\n  * Leverage data and market insights for decision making including content optimization and new concept development.  \n\n\n**_Qualifications  \n  \n_** **Required/Minimum Qualifications  \n**\n  * Bachelor\u0027s Degree in Business, Marketing, Communications, Economics, Public Relations, or related field AND 1+ year(s) integrated marketing (e.g., digital, relationship, social media, campaign), event management, marketing strategy, business planning, marketing operations, or related work experience\n  * OR equivalent experience.  \n\n\n**_Additional Or Preferred Qualifications  \n_**\n  * Bachelor\u0027s Degree in Business, Marketing, Communications, Economics, Public Relations, or related field AND 3+ years integrated marketing (e.g., digital, relationship, social media, campaign), event management, marketing strategy, business planning, marketing operations, or related work experience\n  * OR equivalent experience.\n  * Strong customer centric mindset and demonstrated ability to put the customer first.\n  * Clear and persuasive communication skills, both written and verbal.\n  * Experience with program performance tracking and communications.\n  * Recognized as a self-starter with a bias for action.\n  * Creative problem-solving skills, and a growth mindset approach\n  * Experience managing across highly matrixed organizations, often with competing priorities.\n  * A demonstrated track record of business impact through content\n  * Well-versed in digital marketing best practices, including journey mapping.\n  * Understanding of content disciplines, including SEO, content strategy, and execution.\n  * Preferred, but not required: experience with commercial technology sales process  \n\n\nNarrative   \n  \nIntegrated Marketing IC3 - The typical base pay range for this role across the U.S. is USD $80,900 - $162,200 per year. There is a different range applicable to specific work locations, within the San Francisco Bay area and New York City metropolitan area, and the base pay range for this role in those locations is USD $105,300 - $176,900 per year.   \n  \nMicrosoft has different base pay ranges for different work locations within the United States, which allows us to pay employees competitively and consistently in different geographic markets (see below). The range above reflects the potential base pay across the U.S. for this role (except as noted below); the applicable base pay range will depend on what ultimately is determined to be the candidate\u2019s primary work location. Individual base pay depends on various factors, in addition to primary work location, such as complexity and responsibility of role, job duties/requirements, and relevant experience and skills. Base pay ranges are reviewed and typically updated each year. Offers are made within the base pay range applicable at the time.   \n  \nAt Microsoft certain roles are eligible for additional rewards, including merit increases, annual bonus and stock. These awards are allocated based on individual performance. In addition, certain roles also have the opportunity to earn sales incentives based on revenue or utilization, depending on the terms of the plan and the employee\u2019s role. Benefits/perks listed here may vary depending on the nature of employment with Microsoft and the country work location. U.S.-based employees have access to healthcare benefits, a 401(k) plan and company match, short-term and long-term disability coverage, basic life insurance, wellbeing benefits, paid vacation time, paid sick and mental health time, and several paid holidays, among others.   \n  \nOur commitment to pay equity   \n  \nWe are committed to the principle of pay equity \u2013 paying employees equitably for substantially similar work. To learn more about pay equity and our other commitments to increase representation and strengthen our culture of inclusion, check out our annual Diversity \u0026 Inclusion Report. ( https://www.microsoft.com/en-us/diversity/inside-microsoft/annual-report )   \n  \nUnderstanding roles at Microsoft   \n  \nThe top of this page displays the role for which the base pay ranges apply \u2013 Integrated Marketing IC3. The way we define roles includes two things: discipline (the type of work) and career stage (scope and complexity). The career stage has two parts \u2013 the first identifies whether the role is a manager (M), an individual contributor (IC), an admin-technician-retail (ATR) job, or an intern. The second part identifies the relative seniority of the role \u2013 a higher number (or later letter alphabetically in the case of ATR) indicates greater scope and complexity.   \n  \nMicrosoft is an equal opportunity employer. All qualified applicants will receive consideration for employment without regard to age, ancestry, color, family or medical care leave, gender identity or expression, genetic information, marital status, medical condition, national origin, physical or mental disability, political affiliation, protected veteran status, race, religion, sex (including pregnancy), sexual orientation, or any other characteristic protected by applicable laws, regulations and ordinances. We also consider qualified applicants regardless of criminal histories, consistent with legal requirements. If you need assistance and/or a reasonable accommodation due to a disability during the application or the recruiting process, please send a request via the Accommodation request form.   \n  \nThe salary for this role in the state of Colorado is between $108,200 and $162,200.   \n  \nAt Microsoft, certain roles are eligible for additional rewards, including annual bonus and stock. These awards are allocated based on individual performance. In addition, certain roles also have the opportunity to earn sales incentives based on revenue or utilization, depending on the terms of the plan and the employee\u2019s role. Benefits/perks listed below may vary depending on the nature of your employment with Microsoft and the country where you work. \n",
    "job_functions": [
        "Marketing"
    ],
    "linkedin_internal_id": "content-strategist-at-microsoft-3257696537",
    "location": {
        "city": 'null',
        "country": "United States",
        "latitude": 'null',
        "longitude": 'null',
        "postal_code": 'null',
        "region": "Hawaii",
        "street": 'null'
    },
    "seniority_level": "Mid-Senior level",
    "title": "Content Strategist",
    "total_applicants": 200
}
    # user resume: JSONIFYTool.py
    resume_info = file_to_json()

    # linked in resume: LinkedInCurl.Py
    linkedIn_info = {
    "accomplishment_courses": [],
    "accomplishment_honors_awards": [],
    "accomplishment_organisations": [],
    "accomplishment_patents": [],
    "accomplishment_projects": [
        {
            "description": "gMessenger was built using Ruby on Rails, and the Bootstrap HTML, CSS, and JavaScript framework. It uses a Websocket-Rails integration to post a user\u0027s message content to the page in real time, with no page refresh required. gMessenger also includes custom authentication with three different permissions levels.",
            "ends_at": 'null',
            "starts_at": {
                "day": 1,
                "month": 3,
                "year": 2015
            },
            "title": "gMessenger",
            "url": "http://gmessenger.herokuapp.com/"
        },
        {
            "description": "A task and project management responsive web app utilizing Ruby on Rails - CSS and HTML",
            "ends_at": 'null',
            "starts_at": {
                "day": 1,
                "month": 1,
                "year": 2015
            },
            "title": "Taskly",
            "url": "https://hidden-coast-7204.herokuapp.com/"
        }
    ],
    "accomplishment_publications": [],
    "accomplishment_test_scores": [],
    "activities": [
        {
            "activity_status": "Shared by John Marty",
            "link": "https://www.linkedin.com/posts/johnrmarty_financialfreedom-realestate-technology-activity-6940294635743301632-rsLo",
            "title": "Yesterday I toured a $1.2M property in California that has a large 13K sq ft lot with two homes on it. After 5 minutes of being on-site I\u2026"
        }
    ],
    "articles": [],
    "background_cover_image_url": "https://media.licdn.com/dms/image/C5616AQH9tkBTUhHfng/profile-displaybackgroundimage-shrink_200_800/0/1614530499015?e=2147483647\u0026v=beta\u0026t=VEoCyedtZulnAVYWT9BXfKHi5OFp8avElNjiz8kjSTU",
    "certifications": [
        {
            "authority": "Scaled Agile, Inc.",
            "display_source": 'null',
            "ends_at": 'null',
            "license_number": 'null',
            "name": "SAFe Agile Framework Practitioner - ( Scrum, XP, and Lean Practices in the SAFe Enterprise)",
            "starts_at": 'null',
            "url": 'null'
        },
        {
            "authority": "Scrum Alliance",
            "display_source": 'null',
            "ends_at": 'null',
            "license_number": 'null',
            "name": "SCRUM Alliance Certified Product Owner",
            "starts_at": 'null',
            "url": 'null'
        }
    ],
    "city": "Seattle",
    "connections": 500,
    "country": "US",
    "country_full_name": "United States of America",
    "education": [
        {
            "activities_and_societies": 'null',
            "degree_name": "Master of Business Administration (MBA)",
            "description": 'null',
            "ends_at": {
                "day": 31,
                "month": 12,
                "year": 2015
            },
            "field_of_study": "Finance + Economics",
            "grade": 'null',
            "logo_url": "https://media.licdn.com/dms/image/C560BAQGVi9eAHgWxFw/company-logo_100_100/0/1673448029676?e=2147483647\u0026v=beta\u0026t=NG6ttckXvnS2DX3abTfVACRY2E9Q1EcryNaJLRbE9OE",
            "school": "University of Colorado Denver",
            "school_facebook_profile_url": 'null',
            "school_linkedin_profile_url": "https://www.linkedin.com/school/university-of-colorado-denver/",
            "starts_at": {
                "day": 1,
                "month": 1,
                "year": 2013
            }
        },
        {
            "activities_and_societies": 'null',
            "degree_name": 'null',
            "description": "rails, ruby, rspec, capybara, bootstrap, css, html, api integration, Jquery, Javascript",
            "ends_at": {
                "day": 31,
                "month": 12,
                "year": 2015
            },
            "field_of_study": "School of Software Development",
            "grade": 'null',
            "logo_url": "https://media.licdn.com/dms/image/C560BAQFKNxOZ4X0g8Q/company-logo_100_100/0/1670610916338?e=2147483647\u0026v=beta\u0026t=t7ImfhmsuIJ7HJGHEbPJ2suxdslKhzp9v-5h9_G4sWE",
            "school": "Galvanize Inc",
            "school_facebook_profile_url": 'null',
            "school_linkedin_profile_url": "https://www.linkedin.com/school/galvanize-it/",
            "starts_at": {
                "day": 1,
                "month": 1,
                "year": 2015
            }
        }
    ],
    "experiences": [
        {
            "company": "Freedom Fund Real Estate",
            "company_facebook_profile_url": 'null',
            "company_linkedin_profile_url": "https://www.linkedin.com/company/freedomfund",
            "description": "Our mission is to provide everyday people seeking financial freedom long before the age of 65 with the ability to invest in high yield, short-term real estate investments that were only accessible in the past for a select few wealthy individuals. Each of our single family rehab projects require a minimum investment contribution of only $10K, we have simple terms, no multi-year hold periods, and no fees. With our unique model investors can log into our easy to use website, select the projects that they want to invest in, and get realtime updates on the status of their investments.\n\nWebsite: https://www.freedomfundinvestments.com/home",
            "ends_at": 'null',
            "location": 'null',
            "logo_url": "https://media.licdn.com/dms/image/C560BAQEYxazZM_hXgQ/company-logo_100_100/0/1634934418976?e=2147483647\u0026v=beta\u0026t=wI0YdMmxIctkzvnKxRfuAbT8h5eok_DlUqEph68J37s",
            "starts_at": {
                "day": 1,
                "month": 8,
                "year": 2021
            },
            "title": "Co-Founder"
        },
        {
            "company": "Mindset Reset Podcast",
            "company_facebook_profile_url": 'null',
            "company_linkedin_profile_url": "https://www.linkedin.com/company/mindset-reset-podcast",
            "description": "We dive into the mindsets of the world\u2019s foremost thought leaders and turn them into actionable insights so that others can discover greater happiness, success, and fulfillment.\n\nhttps://podcasts.apple.com/us/podcast/mindset-reset/id1553212607",
            "ends_at": 'null',
            "location": "Denver, Colorado, United States",
            "logo_url": "https://media.licdn.com/dms/image/C560BAQF9QJVQm3SOvA/company-logo_100_100/0/1614527476576?e=2147483647\u0026v=beta\u0026t=m3tx83nMN-E3XQFoJG0Wmch8U4qKnJ9i--5NSAfffC0",
            "starts_at": {
                "day": 1,
                "month": 1,
                "year": 2021
            },
            "title": "Founder"
        }
    ],
    "first_name": "John",
    "follower_count": 'null',
    "full_name": "John Marty",
    "groups": [],
    "headline": "Financial Freedom through Real Estate - LinkedIn Top Voice",
    "languages": [
        "English",
        "Spanish"
    ],
    "last_name": "Marty",
    "occupation": "Co-Founder at Freedom Fund Real Estate",
    "people_also_viewed": [],
    "profile_pic_url": "https://media.licdn.com/dms/image/C5603AQHaJSx0CBAUIA/profile-displayphoto-shrink_800_800/0/1558325759208?e=2147483647\u0026v=beta\u0026t=BluXpPg88xFnU2wMGLjuCUykSk_wKNdh8x3PI9wm6MI",
    "public_identifier": "johnrmarty",
    "recommendations": [
        "Rebecca Canfield\n\n      \n          \n          \n\n\n\n              \n                \n        \n              \n  \n\n      \n          John Marty is a genius at his craft. He is skilled in the art of making people feel empowered to seek out roles that they are qualified for, ask for salaries that they deserve, and creates a kind of pay it forward lifestyle. John helps you to get to places that you only thought were possible for other people. Anyone that is fortunate enough to learn from John should consider themselves extremely lucky. I know I do. ",
        "Zoe Sanoff\n\n      \n          \n          \n\n\n\n              \n                \n        \n              \n  \n\n      \n          John is so focused on helping guide you through an interview process not just for Amazon but on interviewing in general.  I\u0027ve generally done well at interviewing, my skills are top notch now.  John is so focused on on his clients and really goes above and beyond.  John is genuine, knowledgeable, well spoken and non-judgemental.  He is so encouraging, so positive and really easy to talk to.  Thank you John!"
    ],
    "similarly_named_profiles": [
        {
            "link": "https://www.linkedin.com/in/john-martinez-90384a229",
            "location": "San Antonio, TX",
            "name": "John Martinez",
            "summary": "Owner of Fight or Flight Medical Consultants, LLC  , Owner Marty\u2019s Hardwood Works"
        },
        {
            "link": "https://www.linkedin.com/in/senatormarty",
            "location": "St Paul, MN",
            "name": "John Marty",
            "summary": 'null'
        }
    ],
    "state": "Washington",
    "summary": "Most people go through life lost, disengaged, and unhappy at work and in their lives - I\u0027m on a mission to solve that.\n\nI spent 10 years as the founder of Axxis Audio, an electronics company that grew to multi-million dollar sales, which I sold in 2012. At that time, I funneled my earnings into the creation of an Internet of Things company, but numerous factors lead to its demise after 2 hard fought years. \n\nAt 31, I was penny-less, had a baby on the way, and had zero job prospects (despite applying to 150 companies). My desperate situation led me to take a job at Best Buy for $12 an hour while reinventing myself through the completion of an MBA at the University of Colorado, and a 6-month software development boot camp. \n\nAfter graduation, I landed at American Express as a Senior Product Manager and then got poached by Amazon in 2017 (because of my LinkedIn profile). My journey has led to a deep sense of perspective, humility, and purpose that I draw on to help others find clarity, meaning, and happiness in their careers and lives. \n\nCheck out my website for details on my Mindset Reset Podcast, Public Speaking, Consulting, or my free 40 page LinkedIn guide\n\nhttp://www.johnraphaelmarty.com/\n\nFAQ\u0027s\n\nQ: Can you speak at my Company, University, event or podcast?\nA: I\u0027d love to! I\u0027ve shared my message on the future of employment, breaking into big tech, and my personal story of reinventing myself and discovering my sense of purpose (and how you can too!).\n\n\u2611\ufe0f  YouTube Channel #1 (John Marty) : http://www.youtube.com/c/JohnMarty-uncommon\n\u2611\ufe0f  YouTube Channel #2 (Tech Careers for non-engineers: https://www.youtube.com/channel/UC900gMMPLwRGGXSTW1gdZHA\n\nFUN FACTS:\n\u2611\ufe0f I am an Avid cyclist and runner, and I just started learning to skateboard a half-pipe.\n\u2611\ufe0f Into the Enneagram? - I\u0027m a #3 (The Achiever)\n\nLETS CONNECT:\n\u2611\ufe0f Email: JohnRmarty@gmail.com (don\u0027t forget that \"R\"....The other guy gets my emails all the time)",
    "volunteer_work": []
}

    merged_dict = {}
    merged_dict.update(job_info)
    merged_dict.update(resume_info)
    merged_dict.update(linkedIn_info)
    

    # Create a list of non-None JsonSpec instances
    json_spec = JsonSpec(dict_=merged_dict)
    json_toolkit = JsonToolkit(spec=json_spec)

    llm = OpenAI(temperature=0)

    # Create an agent with the single JsonToolkit
    agent = create_json_agent(llm, toolkit=json_toolkit, verbose=True)

    query = """you are given information for the users linkedin profile, their resume, and the job they want to apply to. 
               Based on this information what improvements can the user make on their resume to enhance their chances of getting the job

               return advice in a resume like format               
            """
    result = agent.run(query)
    print(result)
    