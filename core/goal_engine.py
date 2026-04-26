from .semantic_engine import semantic_score


class GoalDecomposer:
    def __init__(self, goal):
        self.goal = goal.lower()
    
    def decompose(self):
        words = self.goal.split()
        
        subgoals = []
        
        if "api" in words:
            subgoals.extend([
                "api overview",
                "api authentication",
                "api endpoints",
                "api examples"
            ])
        
        if "documentation" in words:
            subgoals.extend([
                "documentation overview",
                "usage guide",
                "reference"
            ])
        
        if "guide" in words:
            subgoals.extend([
                "guide overview",
                "getting started",
                "tutorial"
            ])
        
        if "tutorial" in words:
            subgoals.extend([
                "tutorial basics",
                "step by step",
                "examples"
            ])
        
        if "auth" in words or "authentication" in words:
            subgoals.extend([
                "authentication",
                "login",
                "authorization"
            ])
        
        if "install" in words or "setup" in words:
            subgoals.extend([
                "installation",
                "setup guide",
                "configuration"
            ])
        
        if not subgoals:
            subgoals = [self.goal]
        
        return sorted(set(subgoals))


class GoalTracker:
    def __init__(self, subgoals):
        self.subgoals = subgoals
        self.completed = {sg: False for sg in subgoals}
    
    def update(self, text):
        if not text:
            return
        
        for sg in self.subgoals:
            score = semantic_score(text, sg)
            if score > 5:
                self.completed[sg] = True
    
    def get_progress(self):
        total = len(self.subgoals)
        done = sum(self.completed.values())
        return round(done / total, 4) if total > 0 else 0
    
    def get_remaining(self):
        return [k for k, v in self.completed.items() if not v]
    
    def is_complete(self):
        return all(self.completed.values())
    
    def get_completed(self):
        return [k for k, v in self.completed.items() if v]


def refine_goal(context):
    goal = context.get("goal", "")
    entities = context["knowledge"]["entities"]

    keywords = sorted(
        [
            str(entity.get("value", ""))
            for entity in entities
            if isinstance(entity, dict) and entity.get("type") == "keyword"
        ]
    )

    if keywords:
        refined = f"{goal} {' '.join(keywords[:3])}".strip()
        context["goal"] = refined
