
---

```markdown
# Hardware Setup  
## AI Against Litter

---

## 1. Overview
The hardware system is designed to be mounted on a litter picker tool.  
All components are fixed to ensure durability during outdoor use.

---

## 2. Components
- Raspberry Pi 5
- Camera module
- Buzzer
- Push button
- Perfboard
- 40-pin GPIO connector

---

## 3. GPIO Configuration

| Component | GPIO Pin |
|-----------|----------|
| Buzzer    | GPIO17   |
| Button    | GPIO20   |

---

## 4. Assembly Notes
- Components are soldered onto a perfboard
- The perfboard connects directly to the Raspberry Pi GPIO header (2x20)
- The button is placed on top of the tool for easy access
- The camera is aligned with the picking direction

---

## 5. Safety Notes
- Avoid short circuits on the GPIO pins
- Do not power the system while modifying connections
- Use proper strain relief for cables

---

## 6. Prototype Disclaimer
This hardware setup represents a functional prototype intended for academic demonstration.
