# MIMIC-III to RDF

_MIMIC-III to RDF_ is a program that, based on the clinical database [MIMIC-III](https://physionet.org/content/mimiciii/1.4/) and a spatiotemporal data model for epidemiology (see image), generates an RDF knowledge graph and an RDF* knowledge graph of a hospital and the movements of its inpatients inside it. It also generates CSV files to allow the use of the data for other purposes and structures.

<!-- ![Spatiotemporal model for hospital epidemiology](https://github.com/LorenaPujante/MimicToRDF/assets/154461660/ccb2426b-7718-4bb1-bc14-330aabdb4b40) -->
<p align="center">
  <img src="https://github.com/LorenaPujante/MimicToRDF/assets/154461660/ccb2426b-7718-4bb1-bc14-330aabdb4b40" alt="Spatiotemporal model for hospital epidemiology">
</p>

## 1. Data Structure
The data for the knowledge graphs is obtained from MIMIC-III (see [Section 2](#dataAcq)) and organized in two dimensions:
- **Spatial dimension:** The spatial dimension comprises the hospital layout and the healthcare workers (HCWs) organization. Both are fixed.
	- HCWs are organized into Services divided into Hospitalization Units (HU). The Services are the same as in MIMIC-III. HUs are created based on the Service admissions, so there are at most 1,500 admissions per HU. So, if a Service attends 4000 admissions, it will have 3 HUs (4000/1500 = 2.7).
 	- The hospital layout comprises three classes of elements: Beds, Rooms and Corridors. The layout depends entirely on admissions and the HCW organization. Its creation consists of a set of steps with restrictions.
  		- There is one Building with one Floor.
    	- The Floor is organized in two parallel Corridors with Rooms on both sides.
     	- Each Room will have a maximum of 10 Beds.
      	- MIMIC-III organizes data into wards (no Rooms), and we use the admission of the wards to determine the number of Beds, Rooms and Corridors.
      	- The total number of Beds depends on the number of admissions: there must be sufficient Beds in each ward to encompass the maximum number of simultaneous hospitalized patients if we compact all its hospitalizations in just one year. Then, these beds are homogenously distributed between the rooms. For example, if a ward has 16 simultaneous admissions, it will have 16 Beds organized in 2 Rooms, so each Room has 8 Beds.
      	- We have classified Services into 3 groups ([according to their description](https://mimic.mit.edu/docs/iii/tables/services/)): Surgical, Medical and Neonatal.
      	- Rooms are organized into four groups (Surgical, Medical, Mixed and Neonatal) based on the Services that attend patients into them. To determine which group a Room belongs to, we count the number of hospitalizations inside the room cared for by each Service group (for example, a Bed can have a patient attended by a surgical Service and then a patient looked after by a medical Service). The Room will be assigned to the majority group. For example, if into a Room there are 20 Surgical admissions, 35 Medical and 0 Neonatal, it will be a Medical Room. If there are the same number of Surgical and Medical admissions, the Room will be Mixed.  
      	- Rooms are placed into one of the two main corridors depending on its group. A corridor will have only Rooms from the Surgical group, and the other one will have the Rooms from the Mixed, Medical and Neonatal groups (in this order from left to right).
      	- Each corridor is divided into chunks (the actual Corridors from the model), so there are at most 20 Rooms per Corridor.
      	- Finally, the hospital has **156** _Surgical Rooms_ with **1,413** Beds, **23** _Medical Rooms_ with **179** Beds, **56** _Mixed Rooms_ with **510** Beds and **4** _Neonatal Rooms_ with **13** Beds.
      	- The image below is a schematic representation of the hospital layout
   
-  **Temporal dimension:** The temporal dimension comprises the patients' movements inside the hospital in the form of Events. Hospitalization Events represent when a patient is in a specific Bed, Death Events report when a patient dies, and TestMicro Events represent a microbiological test that has been positive for some Microorganism(s). MIMIC-III works with fictional dates, so it is possible to change the years of the dates to a specific period. For example, we want all the Events to be between 2000 and 2025. If you want the result to have only some of the Events, you can select from which years you want the Events. For example, from the previous period, you only want the Events between 2010 and 2020. You can also limit the maximum number of Events. These Events will be distributed equally (as far as possible) between the months. The result may have a slight variation in the number of events. For example, if you want a maximum of 100,000 Events, as a result, you may have 98,500 Events.      

<!--![Schematic representation of the hospital layout](https://github.com/LorenaPujante/MimicToRDF/assets/154461660/4c12d02c-352a-4add-ab93-7e3a3646470d)-->
<p align="center">
  <img src="https://github.com/LorenaPujante/MimicToRDF/assets/154461660/4c12d02c-352a-4add-ab93-7e3a3646470d" alt="Schematic representation of the hospital layout">
</p>


## 2. Data Acquisition <a id='dataAcq'></a>

All the necessary data for _MIMIC-III to RDF_ must be obtained from the MIMIC-III database and organized in a set of CSV files. The file _Input/FileNames.txt_ presents the name that the input files must have.

The file _Input/SQLQueries.txt_ presents a set of queries that can be used to retrieve the data from MIMIC-III. Each query is for a file. The result from each query must be saved as a CSV file, in which the heading should be the same as the result columns of the clause `SELECT` from the query. For example, the `SELECT` clause of the query for the file _microorganisms.csv_ is `SELECT DISTINCT ORG_ITEMID, CONCAT('"', ORG_NAME, '"') AS ORG_NAME`, so the heading of the CSV should be: _ORG_ITEMID,ORG_NAME_

Three input files are already created (_Input/servsEvents.csv_, _Input/wardsAndRooms.csv_, _Input/wardsByType.csv_), but are not complete. They need the data obtained from MIMIC-III. In _Input/SQLQueries.txt_, after the query for each file, there are brief instructions to complete the file with the result.


## 3.Installation
The source code is currently hosted on [github.com/LorenaPujante/MimicToRDF](https://github.com/LorenaPujante/MimicToRDF).

The program is in Python 3.8, and no external packages are needed.


## 4. Execution and Configuration Params
To run the program, in the terminal, go to the folder containing the program and run: `python main.py`

The main function receives as parameters for configuring the result the following:
- _minYearN_, _maxYearN_: Years between which to normalize MIMIC-III dates.
- _minYear_, _maxYear_: Years from which to select the result Events.
- _maxEvents_: Maximum number of Events the result will have.

For example, if we execute: `generateSolution(2000, 2025, 2010, 2010, 125000)`, the program will normalize the years from MIMIC-III between 2000 and 2025, then select those Events that happened in 2010 and, finally, limit the Events to 125,000.

When executing the program, the names of some folders and files of the result have a legend with the configuration parameters at the end. In the previous example, one of the result folders would be: `OutputRDF/Relations_00-25__10-10__125.nt`

In the file _main.py_, the function `main()` has a set of tests for executing the program with different configuration parameters. These parameters can be changed in this function.


## 5. Outcomes
After running the program, the following folders are created:
- _OutputCSV_: Folder with the nodes and edges of the graph in the form of CSV files.
	- Nodes and edges are in different folders: `OutputCSV/Classes.*` (nodes) and `OutputCSV/CSV.*` (edges). Each class of nodes and edges is in a separate file.
- _OutputRDF_: Folder with the nodes and edges of the RDF knowledge graph in the form of N-Triples files.
	- Nodes and edges are in different folders: `OutputRDF/Classes.*` (nodes) and `OutputRDF/CSV.*` (edges). Each class of nodes and edges is in a separate file. Inside each folder, there also is a file with the union of all the nodes (`OutputRDF/Classes.*/Classes_complete.*.nt`) and the union of all the edges (`OutputRDF/Relations.*/Relations_complete.*.nt`), respectively. Finally, the file `OutputRDF/data_complete.*.nt` contains the nodes and edges' union.
- _OutputRDF_star_: Folder with the nodes and edges of the RDF* knowledge graph in the form of N-Triples files (nodes) and Turtle files (edges).
	- Nodes and edges are in different folders: `OutputRDF_star/Classes.*` (nodes) and `OutputRDF_star/CSV.*` (edges). Each class of nodes and edges is in a separate file. Inside each folder, there also is a file with the union of all the nodes (`/Classes.*/Classes_complete.*.nt`) and the union of all the edges (`OutputRDF_star/Relations.*/Relations_complete.*.ttl`), respectively. Finally, the file `OutputRDF_star/data_complete.*.ttl` contains the nodes and edges' union.
- _OutputSummary_: Folder with a summary of the created hospital layout (_description_ and number of the Corridors, Rooms and Beds) and the number of Episodes and Events.  

Repeated runs will replace existing files.

