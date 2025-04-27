def get_recommendations(course: str, struggled_topic: str) -> list:
    """
    Returns a list of study recommendations based on the course and the topic the student is struggling with.
    Includes fallback suggestions if specific matches are not found.
    """
    base_recommendations = {
        "College Algebra": {
            "Quadratic Equations": [
                "Review solving quadratics using the quadratic formula.",
                "Watch this short video on factoring quadratics.",
                "Try practice set #3 from your MDC LMS.",
            ],
            "Linear Equations": [
                "Go over solving multi-step linear equations.",
                "Use a graphing calculator to visualize slope-intercept form.",
                "Complete the linear equations quiz again.",
            ],
        },
        "English Comp I": {
            "Thesis Statements": [
                "Read the MDC guide on crafting strong thesis statements.",
                "Analyze examples of good vs. weak thesis statements.",
                "Submit your draft to the writing lab for feedback.",
            ],
            "Sentence Structure": [
                "Review subject-verb agreement rules.",
                "Use Grammarly to check for run-ons and fragments.",
                "Try the sentence structure self-check worksheet.",
            ],
        }
    }

    recommendations = base_recommendations.get(course, {}).get(struggled_topic)
    if recommendations:
        return recommendations

    if course.lower().startswith("math") or "algebra" in course.lower():
        return [
            f"No specific recommendations found for '{struggled_topic}', but here are some helpful resources:",
            f"Search YouTube: https://www.youtube.com/results?search_query={struggled_topic.replace(' ', '+')}+math+tutorial",
            "Explore Khan Academy: https://www.khanacademy.org/math"
        ]
    elif "english" in course.lower():
        return [
            f"No specific recommendations found for '{struggled_topic}', but try these:",
            "Use Grammarly: https://www.grammarly.com",
            "Explore writing tips: https://owl.purdue.edu/owl/purdue_owl.html"
        ]
    else:
        return [
            f"We couldn't find specific tips for '{struggled_topic}', but try searching online or checking with your instructor.",
            f"Search YouTube: https://www.youtube.com/results?search_query={struggled_topic.replace(' ', '+')}+study+tips"
        ]


def get_resources(subject: str, concept: str) -> list:
    """
    Returns video or worksheet links based on subject and concept.
    If not found, provides a fallback message and dynamic search link.
    """
    lookup = {
        "math": {
            "quadratic_formula": [
                "https://www.khanacademy.org/math/algebra-home/alg-quadratics/alg-solving-quadratics-using-the-quadratic-formula/v/using-the-quadratic-formula",
                "https://www.youtube.com/watch?v=IlNAJl36-10"
            ],
            "polynomial_multiplication": [
                "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:quadratics-multiplying-factoring/x2f8bb11595b61c86:multiply-binomial/v/multiplying-simple-binomials",
                "https://www.youtube.com/watch?v=cEI8DFTe1zc"
            ]
        },
        "english": {
            "thesis_statement": [
                "https://writingcenter.unc.edu/tips-and-tools/thesis-statements/",
                "https://www.youtube.com/watch?v=DFp1uGTXo4Q"
            ]
        },
        "biology": {
            "photosynthesis": [
                "https://www.khanacademy.org/science/ap-biology/cellular-energetics/photosynthesis/v/photosynthesis",
                "https://www.youtube.com/watch?v=hW_gJRHF7lU"
            ]
        }
    }

    resources = lookup.get(subject.lower(), {}).get(concept.lower())
    if resources:
        return resources

    dynamic_subject = subject if subject.lower() in ["math", "english", "biology"] else "general"
    dynamic_search_url = f"https://www.youtube.com/results?search_query={concept.replace(' ', '+')}+{dynamic_subject}+tutorial"

    return [
        f"No specific resources found for '{concept}'.",
        dynamic_search_url
    ]


def get_visual_resources(subject: str, course: str, concept: str) -> list:
    subject = subject.lower().strip()
    concept = concept.lower().strip()

    """
    Returns a list of visual learning tools (e.g. diagrams, interactive tools) based on subject and concept.
    """
    visuals_lookup = {
        "math": {
            "quadratic_equations": [
                "https://www.mathsisfun.com/algebra/quadratic-equation.html",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Quadratic_graph.svg/600px-Quadratic_graph.svg.png"
            ],
            "linear_equations": [
                "https://www.mathsisfun.com/algebra/linear-equations.html",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Linear_equation.svg/600px-Linear_equation.svg.png"
            ],
            "mean_median_mode": [
                "https://www.mathsisfun.com/data/central-measures.html",
                "https://www.youtube.com/watch?v=2pyq0TJmpzs"
            ]
        },
        "biology": {
            "photosynthesis": [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Photosynthesis_en.svg/600px-Photosynthesis_en.svg.png",
                "https://www.youtube.com/watch?v=zWO-bTi6u8M"
            ],
            "cell_structure": [
                "https://cdn.britannica.com/34/72134-050-B10B01D3/Cytoplasm-cell-structures-organelles-Ribosomes-sites-protein.jpg",
                "https://training.seer.cancer.gov/images/anatomy/cells_tissues_membranes/cell_structure.jpg"
            ]
        },
        "english": {
            "thesis_statement": [
                "https://essayshark.com/blog/wp-content/uploads/2019/04/What-Is-a-Thesis-Statement-1024x724.png",
                "https://writingcenter.unc.edu/tips-and-tools/thesis-statements/"
            ]
        }
    }

    return visuals_lookup.get(subject, {}).get(concept, [
        f"No Visuals found for '{concept}'.",
        f"https://www.google.com/search?q={concept.replace(' ', '+')}+diagram+{subject}"
    ])
