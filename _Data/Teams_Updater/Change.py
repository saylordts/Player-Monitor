from dataclasses import dataclass


@dataclass
class Change:
    type: str
    teamName: str
    teamSubtext: str
    canonicalID: str | None = None
    oldProballersID: str | None = None
    newProballersID: str | None = None
    oldFlashscoreID: str | None = None
    newFlashscoreID: str | None = None
    def proballersUpdateText(self) -> str:
        if self.type == "new":
            if self.newProballersID: return f"N/A -> {self.newProballersID}"
            else: return "N/A"
        text = f"{self.oldProballersID}" if self.oldProballersID else "N/A"
        if self.newProballersID: 
            text += f"-> {self.newProballersID}"
        return text
    def flashscoreUpdateText(self) -> str:
        if self.type == "new":
            if self.newFlashscoreID: return f"N/A -> {self.newFlashscoreID}"
            else: return "N/A"
        text = f"{self.oldFlashscoreID}" if self.oldFlashscoreID else "N/A"
        if self.newFlashscoreID: 
            text += f"-> {self.newFlashscoreID}"
        return text
    def proballersChange(self) -> bool:
        return (
            self.newProballersID is not None
            and self.newProballersID != self.oldProballersID
        )
    def flashscoreChange(self) -> bool:
        return (
            self.newFlashscoreID is not None
            and self.newFlashscoreID != self.oldFlashscoreID
        )