from dataclasses import dataclass

import pandas as pd


@dataclass
class Change:
    type: str
    teamName: str
    teamSubtext: str
    tempIndex: int
    tempLink: str
    canonicalID: str | None = None
    oldProballersID: str | None = None
    newProballersID: str | None = None
    oldFlashscoreID: str | None = None
    newFlashscoreID: str | None = None
    def proballersUpdateText(self) -> str:
        if self.type == "new":
            if self.newProballersID: return f"N/A -> {self.newProballersID}"
            else: return "N/A"
        text = f"{self.oldProballersID}" if (not pd.isna(self.oldProballersID) and self.oldProballersID) else "N/A"
        if self.newProballersID: 
            text += f" -> {self.newProballersID}"
        return text
    def flashscoreUpdateText(self) -> str:
        if self.type == "new":
            if self.newFlashscoreID: return f"N/A -> {self.newFlashscoreID}"
            else: return "N/A"
        text = f"{self.oldFlashscoreID}" if (not pd.isna(self.oldFlashscoreID) and self.oldFlashscoreID) else "N/A"
        if self.newFlashscoreID: 
            text += f" -> {self.newFlashscoreID}"
        return text
    def proballersChange(self) -> bool:
        if pd.isna(self.newProballersID):
            return False
        oldProballersID = None if pd.isna(self.oldProballersID) else self.oldProballersID

        return oldProballersID != self.newProballersID
    def flashscoreChange(self) -> bool:
        if pd.isna(self.newFlashscoreID):
            return False
        oldFlashscoreID = None if pd.isna(self.oldFlashscoreID) else self.oldFlashscoreID

        return oldFlashscoreID != self.newFlashscoreID