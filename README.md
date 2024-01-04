# MIMIC-III to RDF

_MIMIC-III to RDF_ is a software that, based on the clinical database [MIMIC-III](https://physionet.org/content/mimiciii/1.4/) and a spatiotemporal data model for epidemiology (see image), generates an RDF knowledge graph and an RDF* knowledge graph of a hospital and the movements of its inpatients inside it. It also generates .csv files to allow the use of the data for other purposes and structures.

![Spatiotemporal model for hospital epidemiology](https://github.com/LorenaPujante/MimicToRDF/assets/154461660/fbd3b30a-4217-4cd2-9ba8-bfdc3535b3c7)

## 1. Data Structure
The data for the knowledge graphs is obtained from MIMIC-III (see [Section 2](#dataAcq)) and organized in two dimensions:
- **Spatial dimension:** The spatial dimension comprises the hospital layout and the healthcare workers (HCWs) organization. Both are fixed.
	- HCWs are organized into Services divided into Hospitalization Units (HU). The Services are the same as in MIMIC-III. HUs are created based on the Service admissions, so there are no more than 1,500 admissions per HU. So, if a Service attends 4000 admissions, it will have 3 HUs (4000/1500 = 2.7).
 	- The hospital layout comprises 3 classes of elements: Beds, Rooms and Corridors. The layout depends completely on admissions and the HCW organization. Its creation consists of a set of steps with restrictions.
  		- There is one Building with one Floor.
    	- The Floor is organized in two parallel Corridors with Rooms on both sides.
     	- Each Room will have a maximum of 10 Beds.
      	- MIMIC-III organizes data into wards (no Rooms), and we use the admission of the wards to determine the number of Beds, Rooms and Corridors.
      	- The total number of Beds depends on the number of admissions: there must be sufficient Beds in each ward to encompass the maximum number of simultaneous hospitalized patients if we compact all its hospitalizations in just one year. Then, these beds are homogenously distributed between the rooms. For example, if a ward has 16 simultaneous admissions, it will have 16 Beds organised in 2 Rooms, so that each Room has 8 Beds.
      	- We have classified Services into 3 groups ([according to their description](https://mimic.mit.edu/docs/iii/tables/services/)): Surgical, Medical and Neonatal.
      	- Rooms are organized into 4 groups (Surgical, Medical, Mixed and Neonatal) based on the Services that attend patients into them. To determine which group a Room belongs to, we count the number of hospitalizations inside the room attended by each Service group (for example, a Bed can have a patient attended by a surgical Service and then a patient attended by a medical Service). The Room will be assigned to the majority group. For example, if into a Room there are 20 Surgical admissions, 35 Medical and 0 Neonatal, it will be a Medical Room. If there are the same number of Surgical and Medical admissions, then the Room will be Mixed.  
      	- Rooms are placed into one of the two main corridors depending on its group. A corridor will have only Rooms from the Surgical group, and the other one will have the Rooms from the Mixed, Medical and Neonatal groups (in this order from left to right).
      	- Each corridor is divided into chunks (the actual Corridors from the model), so there are no more than 20 Rooms per Corridor.
      	- Finally, the hospital has **156** _Surgical Rooms_ with **1,413** Beds, **23** _Medical Rooms_ with **179** Beds, **56** _Mixed Rooms_ with **510** Beds and **4** _Neonatal Rooms_ with **13** Beds.
      	- The image below is a schematic representation of the hospital layout
   
-  **Temporal dimension:** The temporal dimension comprises the patients' movements inside the hospital in the form of Events. Hospitalization Events represent when a patient is in a specific Bed, Death Events report when a patient dies, and TestMicro Events represent a microbiological test that has been positive for some Microorganism(s). MIMIC-III works with fictional dates, so it is possible to change the years of the dates to a specific period. For example, we want all the Events to be between 2000 and 2025. If you don't want the result to have all the Events, you can select from which years you want the Events. For example, from the previous period, you only want the Events between 2010 and 2020. You can also limit the maximum number of Events. For example, you want a maximum of 100,000 Events, which will be distributed equally (as far as possible) between the months.      

![Schematic representation of the hospital layout](https://github.com/LorenaPujante/MimicToRDF/assets/154461660/5319df1f-083a-4f46-8a21-183742e393d3) 	         

## 2. Data Acquisition <a id='dataAcq'></a>
