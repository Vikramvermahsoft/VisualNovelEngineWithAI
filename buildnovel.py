import random
import json
import requests
import os  # For loading env vars

class Agent:
    def __init__(self, name, personality, goals):
        self.name = name
        self.personality = personality
        self.goals = goals
        self.relationships = {}

    def interact(self, other_agent):
        base_score = random.uniform(-0.1, 0.1)
        if self.personality == "kind" and other_agent.personality == "kind":
            base_score += 0.2
        elif self.personality == "deceptive":
            base_score -= 0.1 if random.random() > 0.5 else 0.1
        self.relationships[other_agent.name] = self.relationships.get(other_agent.name, 0) + base_score
        other_agent.relationships[self.name] = other_agent.relationships.get(self.name, 0) + base_score
        return base_score

class Society:
    def __init__(self):
        self.agents = []
        self.event_graph = {
            "friendship": ["alliance", "betrayal"],
            "conflict": ["reconciliation", "escalation"],
            "neutral": ["friendship", "conflict"]
        }
        self.pages = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def generate_timeline(self, num_pages=5, algorithm="probabilistic", api_key=None):
        current_event = {"type": "neutral"}
        for i in range(num_pages):
            # Select agents and event
            agent1, agent2 = random.sample(self.agents, 2) if len(self.agents) >= 2 else (self.agents[0], self.agents[0])
            change = agent1.interact(agent2) if agent1 != agent2 else 0

            # Choose event type based on algorithm
            if algorithm == "rule_based":
                event_type = "friendship" if change > 0 else "conflict"
            elif algorithm == "probabilistic":
                weights = [0.6 if change > 0 else 0.2, 0.4]
                event_type = random.choices(["friendship", "conflict"], weights=weights)[0]
            elif algorithm == "graph_based":
                possible = self.event_graph.get(current_event["type"], ["neutral"])
                event_type = random.choice(possible)
            else:
                event_type = "neutral"
            
            current_event = {
                "type": event_type,
                "agents": [agent1.name, agent2.name] if agent1 != agent2 else [agent1.name],
                "change": change
            }

            # LLM for dialogue and choices
            narrative = self._call_llm(current_event, api_key) if api_key else {
                "dialogue": [
                    ["Narrator" if agent1 == agent2 else agent1.name, f"{agent1.name} feels {event_type} towards {agent2.name}.", 0],
                    ["Narrator" if agent1 == agent2 else agent2.name, f"Their bond shifts by {change:.2f}.", 0]
                ],
                "choices": [
                    {"text": "Encourage", "next_page": f"page{i+2}" if i+2 < num_pages else f"page{i+1}"},
                    {"text": "Disrupt", "next_page": f"page{i+3}" if i+3 < num_pages else f"page{i+1}"}
                ] if i < num_pages - 1 else []
            }

            # Audio based on event
            audio = []
            if i == 0:
                audio = [["PLAY", f"{event_type}.mp3"]]
            elif i == num_pages - 1:
                audio = [["STOP", f"{event_type}.mp3"]]

            # Images (placeholder; map to agent sprites or event-based BGs)
            images = [f"scene_{i+1}.png"]  # Single BG
            if len(current_event["agents"]) > 1:
                images += [f"{current_event['agents'][0].lower()}_1.png", f"{current_event['agents'][0].lower()}_2.png",
                          f"{current_event['agents'][1].lower()}_1.png", f"{current_event['agents'][1].lower()}_2.png"]
            else:
                images += [f"{current_event['agents'][0].lower()}_1.png", f"{current_event['agents'][0].lower()}_2.png"]

            # Build page
            page = [
                narrative["dialogue"],  # [ ["speaker", "text", 0], ... ]
                audio,                 # [ ["PLAY", "file.mp3"], ... ]
                images,                # [ "bg.png", "sprite1.png", ... ]
                narrative["choices"]   # [ {"text": "Option", "next_page": "pageX"}, ... ]
            ]
            self.pages.append(page)

        # Wrap in a single chapter (array) for timeline.json
        timeline = {f"page{i}": page for i, page in enumerate(self.pages)}
        return [timeline]  # Single chapter; extend to multiple if needed

    def _call_llm(self, event, api_key):
        if not api_key:
            api_key = os.environ.get('GROQ_API_KEY')
            if not api_key:
                print("Warning: GROQ_API_KEY not set; using fallback narrative.")
                return {
                    "dialogue": [
                        [event["agents"][0], f"I sense {event['type']} with {event['agents'][1] if len(event['agents']) > 1 else 'myself'}.", 0],
                        ["Narrator", f"Their relationship shifts by {event['change']:.2f}.", 0]
                    ],
                    "choices": [
                        {"text": "Support", "next_page": "page2"},
                        {"text": "Oppose", "next_page": "page3"}
                    ]
                }

        system_prompt = """
        You are a narrative generator for a visual novel. Generate dialogue (2-3 lines) and 2 choices (if applicable) based on the event.
        Format response strictly as JSON: {"dialogue": [["speaker", "text", 0], ...], "choices": [{"text": "Option", "next_page": "pageX"}, ...]}.
        Dialogue should be natural, reflective, and fit a surreal society simulation. Use agent names as speakers or "Narrator".
        """
        
        user_prompt = f"""
        Event: {event['type']} between {', '.join(event['agents'])}, relationship change: {event['change']:.2f}.
        Generate 2-3 dialogue lines and 2 branching choices (next_page as page2/page3). Keep it concise and engaging.
        """

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",  # Open-source Llama 3 model; swap as needed
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        try:
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            # Parse the content (strip any markdown if present)
            content = result["choices"][0]["message"]["content"].strip('```json\n').strip('```')
            return json.loads(content)
        except Exception as e:
            print(f"Groq API error: {e}")
            # Fallback
            return {
                "dialogue": [
                    [event["agents"][0], f"Let's embrace this {event['type']} moment.", 0],
                    ["Narrator", f"A subtle shift in the society's fabric: {event['change']:.2f}.", 0]
                ],
                "choices": [
                    {"text": "Deepen the bond", "next_page": "page2"},
                    {"text": "Introduce tension", "next_page": "page3"}
                ]
            }

# Example usage
if __name__ == "__main__":
    society = Society()
    society.add_agent(Agent("Alice", "kind", "friends"))
    society.add_agent(Agent("Bob", "ambitious", "power"))
    society.add_agent(Agent("Clara", "deceptive", "chaos"))

    timeline = society.generate_timeline(num_pages=5, algorithm="graph_based")
    with open("timeline.json", "w") as f:
        json.dump(timeline, f, indent=2)

    print("Generated timeline.json for VisualNovelEngine using Groq!")