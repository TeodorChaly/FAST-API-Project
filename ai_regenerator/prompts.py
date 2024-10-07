import json
import os
import random

from ai_regenerator.ai_api_env import API_endpoint
from ai_regenerator.system_prompts import create_prompt
from languages.language_json import language_json_read


def json_loader():
    folder_name = "news_json"
    file_name = f"{folder_name}/crypto.json"
    with open(f"../{file_name}", 'r') as file:
        articles = json.load(file)
    return articles


async def ai_generator_function(text, language, list_of_categories):
    try:
        system_fine_tuning = create_prompt(language, list_of_categories)
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},
                {"role": "user", "content": text},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error during generation: {e}')
        return None


async def ai_category_function(topic_name, additional_info=None):
    try:
        system_fine_tuning = f"""You are creating a news/blog site.
                     And you have to create a JSON-response list, that contains from 20 sub-categories of main category
                     /topic - {topic_name}.
                     (sub-categories must cover 100% of articles of the topic {topic_name}).
                     Here is additional info about the topic it it will help you to create sub-categories:
                     {additional_info} 
                     JSON result format:
                     [
                     "category",
                     "category2", # If you want to use two words, separate them with _ (underscore)
                     "other" # at the end necessary add category other 
                     ]
                     please try to think abstractive and use wide categories name
                     all object must be in lower case. Ouput must be in JSON format and  Without ```json.
                     Here is main topic:"""
        print("start")
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": topic_name},
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None


async def ai_category_for_multiple_languages(language, main_list_of_categories, topic):
    try:
        system_fine_tuning = f"""I am crating news/blog site about this topic {topic}. 
                     I will give you json list and your task to create new JSON file, that looks like this:
                    {{
                    given_category: {{
                    "translated_name":"given_category_translated to {language}", # This field must be 1-2 words and and try to use no longer than 12-14 char. 
                    "translated_category_seo_title": "given_category_seo_title_translated to {language}",  # An SEO title no longer than 50 characters without quotes, reflecting category and being engaging
                    "translated_category_seo_description": "given_category_seo_description_translated to {language}" # An SEO description no longer than 170 characters, briefly describing category
                    }}, 
                    and so on.
                    }}
                    from categories and language that i will give you. Please keep the same structure.
                    Output must be in JSON format and  Without ```json."""
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": main_list_of_categories},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None


async def ai_main_config_for_multiple_languages(language, topic, additional_info=None):
    try:
        system_fine_tuning = f"""I will give you language and you tusk is to translate (or generate) this text to given langauge (but don't translate word for word, but make the meaning clear.) and save it in this json format:
         {{
            "main_page":{{
            "seo_title": "generate here SEO title about main page (list of news) in {topic} topic. And here is additional info if it is helpful - {additional_info}"
            "seo_description":"generate here SEO description about main page (list of news) in {topic} topic. And here is additional info if it is helpful - {additional_info}"
            }},
            "other":"other",
            "read_more": "read more",
            "popular":"popular",
            "more_popular_post":"More_popular_post",
            "popular_posts":"Popular Posts",
            "more_post":"More Post",
            
            
            "read_more":"Read more",
            "trending_topic": "Trending_topic",
            "home": "Home",
            "news": "News",
            "stories": "Stories",
            "popular_stories": "Popular Stories",
            "prev_post":"Prev Post",
            "next_post":"Next Post",
            "by":"By",
            "content_writer":"Content Writer",
            "content_writer_text":"Hi there, i am"
            }}
         
            Output must be in JSON format and Without ```json. Here is language"""
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": language},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None


async def ai_main_terms_function(topic, additional_info, site_domain, site_name, categories):
    try:
        current_file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        folder_name = os.path.join(current_file_path, "languages")
        folder_name2 = os.path.join(folder_name, "languages.json")

        founded_year = [2020, 2021, 2022, 2023]
        year = founded_year[random.randint(0, 3)]

        with open(folder_name2, "r", encoding="utf-8") as file:
            languages = json.load(file)

        about_us = await ai_generate_about_us(languages, topic, additional_info, site_domain, site_name, year,
                                              categories)
        new_json = {}

        try:
            new_json["about_us"] = about_us
        except json.JSONDecodeError as e:
            print(f"Error during about us loading: {e}")

        privacy_policy = await ai_generate_privacy_policy(languages, topic, additional_info, site_domain, site_name,
                                                          year, categories)
        try:
            new_json["privacy_policy"] = privacy_policy
        except json.JSONDecodeError as e:
            print(f"Error during privacy policy loading: {e}")

        terms_of_use = await ai_generate_terms_of_use(languages, topic, additional_info, site_domain, site_name, year,
                                                      categories)

        try:
            new_json["terms_of_use"] = terms_of_use
        except json.JSONDecodeError as e:
            print(f"Error during terms of use loading: {e}")

        return new_json

    except Exception as e:
        print(f'Error during generation terms: {e}')
        return None


async def ai_generate_about_us(SiteLanguages, SiteTheme, BriefDescription, SiteDomain, SiteName, FoundedYear,
                               categories):
    try:

        prompts = f"""Craft an in-depth and engaging "About Us" section for a small but growing website. The tone should be professional, yet approachable, highlighting the unique aspects of the website while maintaining a sense of ambition and future growth. The text should appeal to the audience by showcasing the site's strengths and emphasizing its value. The focus should be on building trust, showcasing expertise, and hinting at future potential.

Details to include:
Brief Description of the Website: {BriefDescription}
Languages of the Website: {SiteLanguages}
General Theme/Focus of the Website: {SiteTheme}
Site Name/Domain: {SiteName}
Founded year: {FoundedYear}
Categories: {categories}

The following elements must be integrated:
Introduction and Founding:

Begin by introducing the website, including when it was founded or launched. Explain what inspired the creation of the site and the core purpose behind it. The introduction should give a sense of what the site offers and why it stands out.
Multilingual Accessibility:

Highlight the fact that the website operates in {SiteLanguages}. Emphasize how this multilingual approach allows the site to cater to a diverse, global audience, making the content more accessible to people from various regions and language backgrounds.
Themes and Areas of Expertise:

Dive into the general theme or focus of the site. Clearly describe the site's main topics or areas of expertise (such as {SiteTheme}) and explain how the content is structured to provide valuable resources, articles, or services around this area. Provide examples of the type of content or resources available.
Audience and Community:

Specify who the primary audience is (e.g., individuals, businesses, professionals). Describe how the site serves their needs and provides solutions or insights that are relevant to their interests or professional goals. Touch on the growing community of readers or users who rely on the site for information, inspiration, or services.
Unique Features and Benefits:

Highlight what sets the website apart from other similar platforms. This could include a focus on quality content, a commitment to impartiality, user-friendly design, innovative tools or resources, or any specialized services. Mention any standout features that visitors can expect when using the site.
Mission and Values:

Mention the key mission of the site and its core values, such as integrity, quality, or transparency. Explain how these values guide the content creation and overall direction of the site, ensuring that the audience feels they can trust the information and services provided.
Future Ambitions and Goals:

Discuss the website’s growth trajectory and its future ambitions. This section should focus on what the website hopes to achieve, such as expanding its content offerings, reaching new audiences, or launching new features. This shows readers that the site is forward-thinking and committed to continuous improvement.
Invitation to Explore:

End with an invitation for visitors to explore the website, follow its journey, or become part of the growing community. Encourage engagement, whether it’s through subscribing, contacting the team, or sharing the content."""

        system_fine_tuning = prompts
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": "Write in english"},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation about us: {e}')
        return None


async def ai_generate_terms_of_use(SiteLanguages, SiteTheme, BriefDescription, SiteURL, CompanyName, FoundedYear,
                                   categories, CompanyAddress="London"):
    try:

        prompt = f"""""Create a comprehensive 'Terms of Use' document for {CompanyName}, located at {CompanyAddress}, operating both a website at {SiteURL}. This document should follow the standard legal structure used by major online services and address the following sections in detail:

Introduction and Acceptance of Terms: Begin with a formal introduction stating that the use of {CompanyName}'s services, including {SiteURL}, constitutes acceptance of these terms. Include the date of the last update and clarify that these terms apply to all users, whether registered or not.

Modifications to the Terms: Clearly explain that {CompanyName} reserves the right to modify these terms at any time. Users will be notified of material changes via the website, app, or email. Continued use of the services after changes are posted will constitute acceptance of the updated terms.

Eligibility Requirements: Specify the legal age required to use the services (e.g., 18 years or older) and any restrictions based on user jurisdiction. Include a statement regarding the responsibility of users to ensure their compliance with local laws.

User Account and Security: Describe the process for creating a user account, the responsibilities associated with maintaining account confidentiality, and the user’s obligation to notify {CompanyName} in case of unauthorized access. Include details on account suspension or termination in case of a breach of the terms.

Use of Services and Restrictions:

Permitted Use: Outline what users are allowed to do on the platform, such as browsing content, downloading materials for personal use, etc.
Prohibited Activities: Provide a list of prohibited actions, including posting illegal or harmful content, engaging in fraud, using automated bots or data mining tools, and interfering with the proper functioning of the services.
Content Ownership and Intellectual Property:

{CompanyName}'s Content: State that all content provided by {CompanyName} (text, images, logos, etc.) is the intellectual property of {CompanyName} or its licensors and is protected by copyright, trademark, and other intellectual property laws.
User-Generated Content: Explain that users retain ownership of any content they post but grant {CompanyName} a perpetual, non-exclusive, royalty-free license to use, reproduce, modify, and distribute their content across the platform. Users also waive any moral rights to the content they submit.
Third-Party Links and Content: Acknowledge that the services may contain links to third-party websites or applications, but {CompanyName} is not responsible for their content or accuracy. Include a disclaimer that use of third-party services is at the user’s own risk.

Paid Services and Subscription Terms: If applicable, outline the terms regarding any paid features or subscription models:

Billing and Payments: Describe the billing process, recurring payments, and how to update payment methods.
Refunds and Cancellations: Provide a clear policy for refunds, cancellations, and how users can manage their subscription.
Privacy and Data Use: Refer to {CompanyName}'s Privacy Policy, which governs the collection, storage, and use of user data. Include a link to the full Privacy Policy and mention any user rights regarding personal data (e.g., access, correction, deletion).

Termination of Service: Reserve the right to terminate or suspend a user’s account at {CompanyName}'s sole discretion for any violation of the terms. Explain the consequences of termination, including loss of access to content and services.

Disclaimers and Limitation of Liability:
No Warranty: State that {CompanyName} provides its services "as is" without warranties of any kind, whether express or implied.
Limitation of Liability: Limit {CompanyName}’s liability for any damages incurred by users through their use of the services to the maximum extent permitted by law.
Indemnification: Require users to indemnify {CompanyName} from any claims, damages, or losses resulting from their violation of the terms or misuse of the services.
Governing Law and Dispute Resolution:

Specify the governing law (e.g., the jurisdiction in which {CompanyName} operates) and mention that any legal disputes will be settled under these laws.
Arbitration: Include a clause requiring disputes to be resolved through binding arbitration instead of in court. Optionally, allow for claims in small claims court.
Class Action Waiver: Explicitly state that users agree to resolve disputes individually and waive their right to participate in any class action lawsuit.
Miscellaneous:

Severability: State that if any part of the terms is found to be unenforceable, the remaining sections will remain in effect.
Entire Agreement: Mention that these terms represent the entire agreement between {CompanyName} and the user regarding the use of the services, superseding any prior agreements.
Ensure the language is formal, legally accurate, and user-friendly, with a logical flow that mirrors established patterns from major websites. Provide clear sections with concise headers for easy navigation.
"""

        system_fine_tuning = prompt
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": "Write in english"},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error during generation privacy policy: {e}')
        return None


async def ai_generate_privacy_policy(SiteLanguages, SiteTheme, BriefDescription, SiteDomain, SiteName, FoundedYear,
                                     categories):
    try:
        prompt = """"Write a Privacy Policy that clearly explains how a company collects, uses, and protects personal data. The policy should cover the following key sections:

Introduction: Begin with a statement that emphasizes the company’s commitment to protecting user privacy and describe the purpose of the policy. Mention that the policy applies to all users of the company’s services (website, apps, etc.).

Information We Collect:

List the types of personal information collected (e.g., contact data, account information, payment details, etc.).
Include specific categories like personal identifiers, device information, and any other user-generated content (such as comments, posts, or feedback).
Mention whether any sensitive data (e.g., location data, demographic information) is collected and how.
How We Collect Information:

Explain how the data is collected (e.g., when users interact with the service, create accounts, submit forms, or browse the site).
Include mention of cookies, web beacons, or other tracking technologies, and clarify how they work.
Note any third-party data sources (such as social media integrations or advertising partners).
How We Use Your Information:

Detail how the data will be used (e.g., service provision, user experience customization, analytics, marketing, or communication).
Include the lawful basis for processing under applicable regulations, such as consent, legitimate interest, or contractual obligations.
Information Sharing and Disclosure:

Identify who the company may share data with (e.g., service providers, business partners, advertising networks).
Include any legal obligations that might require data sharing (e.g., compliance with law enforcement).
Mention third-party services integrated into the platform, and advise users to review external privacy policies where applicable.
Cookies and Tracking Technologies:

Provide information about the use of cookies and other tracking technologies.
Describe how users can control or disable cookies via their browser settings or other tools.
Mention third-party analytics tools (e.g., Google Analytics) and how they track user behavior.
User Rights and Choices:

List the rights users have regarding their personal data (e.g., access, correction, deletion, restriction of processing).
Include options for opting out of marketing communications and targeted advertising.
Mention any mechanisms for submitting requests, such as forms or email contact.
Data Security and Retention:

Explain how user data is protected (e.g., encryption, firewalls, secure data storage).
Mention how long data is retained and the criteria for determining retention periods.
State what happens to user data after account deletion or service termination.
International Data Transfers:

If applicable, explain how personal data may be transferred across borders and the legal safeguards (e.g., Standard Contractual Clauses) used to protect the data during international transfers.
Children’s Privacy:

Include a section on handling children’s data if the service is accessible to minors, adhering to regulations like COPPA or GDPR.
Changes to the Privacy Policy:

Describe how users will be informed about updates to the policy.
Mention the effective date of the policy and encourage regular review for any changes.
Contact Information:

Provide clear contact details (e.g., email, physical address) for users to reach the company’s Data Protection Officer (DPO) or privacy team for questions or requests.
Tone and Style:

Use clear and straightforward language, avoiding technical jargon.
Ensure transparency, emphasizing user control over personal information.
Follow legal obligations based on relevant privacy laws (e.g., GDPR, CCPA)."""
        system_fine_tuning = prompt
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": "Write in english"},
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error during generation privacy policy: {e}')
        return None


async def ai_translate_terms(json_terms, language):
    news_json = {}
    for key in json_terms:
        try:
            print(f"Translating {key} to {language}")
            completion = API_endpoint.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system",
                     "content": f"Translate this text to {language}"},
                    {"role": "user", "content": json_terms[key]},
                ]
            )
            news_json[key] = completion.choices[0].message.content
        except Exception as e:
            print(f'Error during translation: {e}')
    return news_json


async def ai_translate_config(content, language):
    try:
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": f"Translate this text to {language}. Output must be in correct JSON format."},
                {"role": "user", "content": content},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error during translation: {e}')


async def ai_generate_team():
    format_of_person = {"Name Surname":
                            {"name": "Name",
                             "surname": "Surname",
                             "feature": "unique feature",
                             "about me": "info about person",
                             "image": "-",
                             "position": "job position/job title"
                             }
                        }
    lang_list = ['turkish', "russian"]
    prompt = f""""You are creating a team for website. Team size is from 5 to 10 people (Choose the number of people as you see fit). 
    The website is targeted at the following languages: {lang_list}, so make sure that almost every team member has a name from one of these languages (or countries).
    Here’s how the team should look: 
    1 - Founder/Owner,
    70% - Copywriter/Journalist,
    25% - Translator (Ideally, there should be at least as many translators as there are languages)    
    
    Output must be in JSON format and  Without ```json. Here is the format of person:
    {{"0":
          {{"name": "Name of person",  
          "surname": "Surname of person",
          "feature": "Unique writing style (for copywriters) or some unique feature (for the founder or translator, leave blank -)",
          "about me": "Information about person. Come up with some information about these individuals (preferably related to work).",
          "image": "Leave it as '-'",
          "position": "job position/job title"
          }},
          "1": {{...}}
     }}
     Write in English
    """
    try:
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": prompt},
                {"role": "user", "content": prompt},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error during translation: {e}')

    return {"team": "team"}


async def ai_translate_team(json_team, language):
    try:
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": f"Translate this JSON to {language} and output must be in correct JSON format. Without ```json."},
                {"role": "user", "content": json_team},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f'Error during translation: {e}')



