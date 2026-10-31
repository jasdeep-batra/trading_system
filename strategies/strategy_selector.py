class StrategySelector:


    def __init__(self, registry):

        self.registry = registry



    def select(self, regime):


        if regime == "TRENDING":

            return [

                self.registry.get("trend"),

                self.registry.get("breakout"),

                self.registry.get("smc")

            ]


        elif regime == "RANGING":

            return [

                self.registry.get("pullback")

            ]


        return []