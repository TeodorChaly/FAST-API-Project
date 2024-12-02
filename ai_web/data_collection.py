import asyncio

from ai_web.get_web_media import search_youtube_video, search_image
from ai_web.web_ai import *
from ai_web.web_prompts import *


async def general_info(product):
    system_prompt = get_general_info_prompt(product)
    content, citations = await perplexity_api(product, system_prompt)
    return content, citations


async def competitors_info(product):
    system_prompt = get_competitors_info_prompt(product)
    content, citations = await perplexity_api(product, system_prompt)
    return content, citations


async def get_structure(general_content, competitors_content):
    print("General Content:", general_content)
    print("Competitors Content:", competitors_content)
    # print(await get_html_structure_prompt())
    # html_structure = await openai_api("test", "test")
    html_structure = {
        "title": "2025 Toyota 4Runner: A Comprehensive Review of the New Features and Performance",
        "sections": [
            {
                "h2": "Redesign and New Features",
                "description": "The 2025 Toyota 4Runner introduces a complete redesign with improved performance and updated aesthetics, offering a fresh take on an iconic SUV.",
                "subsections": [
                    {
                        "h3": "New Platform and Design",
                        "content": "The 2025 4Runner is built on a new platform shared with the Toyota Tacoma, enhancing handling and performance. The exterior retains the rugged 4Runner look but adds modern touches, including a bold grille and LED lighting.",
                        "image": "Image description: The new front fascia of the 2025 Toyota 4Runner with updated grille and LED lighting."
                    },
                    {
                        "h3": "Interior Modernization",
                        "content": "The interior offers a significant upgrade with a standard 8-inch touchscreen and an optional 14-inch display, featuring Toyota's latest infotainment system. Enhanced safety features like Toyota Safety Sense 3.0 are included.",
                        "table": {
                            "headers": ["Feature", "Description"],
                            "rows": [
                                ["Touchscreen", "8-inch standard, 14-inch optional"],
                                ["Safety Features", "Toyota Safety Sense 3.0"],
                                ["Connectivity", "Wireless Apple CarPlay and Android Auto"]
                            ]
                        },
                        "image": "Image description: The 2025 Toyota 4Runner's interior showing the 14-inch touchscreen and modern dashboard layout."
                    }
                ]
            },
            {
                "h2": "Performance Specifications",
                "description": "The 2025 Toyota 4Runner offers two engine options, a turbocharged four-cylinder and a hybrid variant, both of which provide substantial performance improvements over previous models.",
                "subsections": [
                    {
                        "h3": "Engine Options and Performance",
                        "content": "The 2025 4Runner comes with a 2.4-liter turbocharged four-cylinder engine producing 278 horsepower and 317 lb-ft of torque, or an i-FORCE MAX hybrid engine that generates 326 horsepower and 465 lb-ft of torque.",
                        "table": {
                            "headers": ["Engine", "Horsepower", "Torque", "Transmission"],
                            "rows": [
                                ["2.4L Turbocharged", "278 hp", "317 lb-ft", "8-speed automatic"],
                                ["i-FORCE MAX Hybrid", "326 hp", "465 lb-ft", "8-speed automatic"]
                            ]
                        }
                    },
                    {
                        "h3": "Towing Capacity and Transmission",
                        "content": "The 2025 4Runner boasts a maximum towing capacity of 6,000 pounds, an increase from previous models, and both engine options come with an 8-speed automatic transmission for improved efficiency and performance.",
                        "image": "Image description: The Toyota 4Runner towing a trailer, demonstrating its maximum towing capacity."
                    }
                ]
            },
            {
                "h2": "Trim Levels and Options",
                "description": "The 2025 Toyota 4Runner offers various trims to suit different preferences, from base models to specialized off-road versions.",
                "subsections": [
                    {
                        "h3": "Overview of Available Trims",
                        "content": "The 2025 4Runner is available in multiple trims, including SR5, TRD Sport, TRD Off-Road, Limited, TRD Pro, and the new Trailhunter, each designed to offer unique features for different users.",
                        "table": {
                            "headers": ["Trim", "Target Audience", "Key Features"],
                            "rows": [
                                ["SR5", "General use", "Standard features, practical design"],
                                ["TRD Sport", "Off-road enthusiasts", "Enhanced suspension, off-road styling"],
                                ["TRD Off-Road", "Rugged terrain", "Specialized off-road equipment"],
                                ["Limited", "Luxury seekers", "Premium materials, advanced tech"],
                                ["TRD Pro", "Serious off-roaders", "Top-tier off-road equipment"],
                                ["Trailhunter", "Overlanding enthusiasts", "Heavy-duty off-road enhancements"]
                            ]
                        }
                    }
                ]
            },
            {
                "h2": "Off-Road Capabilities",
                "description": "The 2025 Toyota 4Runner is built for off-road enthusiasts, offering several features to enhance its performance in challenging terrains.",
                "subsections": [
                    {
                        "h3": "Key Off-Road Features",
                        "content": "The 2025 4Runner includes specialized off-road gear like the Stabilizer Disconnect Mechanism, Multi-Terrain Select, and CRAWL Control, which help the vehicle navigate rough terrain with ease.",
                        "table": {
                            "headers": ["Feature", "Description"],
                            "rows": [
                                ["Stabilizer Disconnect Mechanism", "Improves wheel articulation on rough terrain"],
                                ["Multi-Terrain Select", "Optimizes performance on different surfaces"],
                                ["CRAWL Control", "Helps maintain low-speed traction in challenging conditions"]
                            ]
                        }
                    },
                    {
                        "h3": "Off-Road Performance Comparison",
                        "content": "Compared to rivals like the Jeep Wrangler, the 4Runner stands out with its advanced off-road technologies, making it a top choice for outdoor enthusiasts.",
                        "image": "Image description: The 2025 Toyota 4Runner navigating rugged terrain with Multi-Terrain Select engaged."
                    }
                ]
            },
            {
                "h2": "Expert Opinions",
                "description": "Expert reviews highlight the 2025 Toyota 4Runner's balance of rugged off-road capabilities with modern features and technology.",
                "subsections": [
                    {
                        "h3": "What Experts Are Saying",
                        "content": "Critics praise the 2025 4Runner for its significant performance upgrades, modernized interior, and impressive off-road capabilities, making it a versatile choice for various lifestyles.",
                        "image": "Image description: A professional review of the 2025 Toyota 4Runner being conducted on a test track."
                    }
                ]
            },
            {
                "h2": "Sustainability Focus",
                "description": "The 2025 Toyota 4Runner incorporates sustainable practices, including eco-friendly materials and improved fuel efficiency from the hybrid powertrain.",
                "subsections": [
                    {
                        "h3": "Eco-Friendly Materials and Hybrid Efficiency",
                        "content": "Toyota has focused on reducing the environmental impact of the 2025 4Runner, using eco-friendly materials in the vehicle's construction and improving fuel efficiency with the i-FORCE MAX hybrid engine.",
                        "table": {
                            "headers": ["Sustainability Feature", "Benefit"],
                            "rows": [
                                ["Eco-friendly materials", "Reduced environmental impact in production"],
                                ["Hybrid powertrain", "Improved fuel efficiency and lower emissions"]
                            ]
                        }
                    }
                ]
            }
        ],
        "video": "Video description: A detailed walkaround of the 2025 Toyota 4Runner, showcasing its off-road capabilities, interior features, and new platform."
    }

    return html_structure


async def get_video_and_images(html_structure):
    print(search_youtube_video(html_structure["video"]))

    images = []
    for section in html_structure["sections"]:
        for subsection in section["subsections"]:
            if "image" in subsection:
                images.append(subsection["image"])
    for i in images:
        print(search_image(i), i)
    pass  # return {video: "url", images: [{alt: "url", alt: "url"}]}


async def get_content():
    pass  # return {content: "content"}


async def main(topic):
    general_task = asyncio.create_task(general_info(topic))
    competitors_task = asyncio.create_task(competitors_info(topic))

    general_content, general_citations = await general_task
    competitors_content, competitors_citations = await competitors_task

    print("General Info:", general_content, general_citations)
    print("Competitors Info:", competitors_content, competitors_citations)
    await get_structure(general_content, competitors_content)


if __name__ == "__main__":
    main_topic = "example_topic"
    a = asyncio.run(get_structure(1, 1))
    b = asyncio.run(get_video_and_images(a))
