### SEAT - Data Generator & Max. Card. Matching using CPLEX

It is recommended to set up a virtual environment first using the following commands:
 * `virtualenv <name>`
 * `source <name>/bin/activate`
 * `pip install -r requirements.txt`

---

Run the following terminal command (requires python3) to generate a SEAT instance:

`python3 generate_instance_seat.py <n1> <n2> <k_low> <k_high> <outputfolder>`

Where n1 is the number of residents/students, n2 is the number of hospitals/courses, k_low & k_up are the range for length of resident/student preference lists and outputfolder is the folder to which the instance is generated. Note that the instance generated corresponds to the master model, where the preference lists of students are courses are ordered based on a master list.

---

Run the following command to generate the max. cardinality LP file for an instance and solve the LP using CPLEX solver (must be separately installed from IBM website).

`python3 run_cplex.py <input_dir>`

Where input_dir corresponds to the folder containing the instance. On execution it automatically generates max_card_lp.txt file into the same directory and then invokes CPLEX to solve the LP and its output matching obtained is written to input_dir/output.csv file.
