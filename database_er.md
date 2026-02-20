![Crow's Foot Diagram](ProjectPtB.png)


## Entity Classification
### Strong Entities
Country - Contains what country is being referenced and the population. <br>
Region - Contains the World Health Organization classified region. <br>
Vaccine - Contains what brand of vaccine is being used. <br>
### Weak Entities
InfectStatus - The current total numbers of infected individuals as well as the number of those who have died and recovered from COVID in the country. Dependent on Country. <br>
NewInfect - The recent additions to the number of infected, recovered, and diseased patients of COVID for the country. Dependent on Country. <br>
CountryProfile - Extra country information not typically needed. Dependent on Country. <br>
### Associative Entity
CountryVaccine - Stores the dosage amount, starting date of the vaccination, and the usage percentage for the population for each vaccine of each country. Relates Vaccine to Country. <br>

## Relationships
One-to-Many (1:M)
  - Region → Country  
  - Country → InfectStatus  
  - Country → NewInfect  

One-to-One (1:1)
  - Country ↔ CountryProfile  

Many-to-Many (M:N)
  - Country ↔ Vaccine (resolved by CountryVaccine)
## Attribute Requirements
Identifier: CON_ID, REG_ID, VAC_ID <br>
Single-Valued: ISO_CODE <br>
Mandatory: CON_NAME <br>
Optional: VAC_START_DAY, GDP

## User Groups
Public Health Analyst- Make conclusions on the world's health levels based on the data <br>
Researcher- Perform trend analysis across countries <br>
Administrator- Manages the data structure and ensures it is accurately updated <br>
