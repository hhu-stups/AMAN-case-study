MACHINES := \
	M0_AMAN_Update_prob_mc_mch \
	M1_Landing_Sequence_prob_mc_mch \
	M2_Hold_Button_prob_mc_mch \
	M0_AMAN_Update_prob_mc2_mch \
	M1_Landing_Sequence_prob_mc2_mch \
	M2_Hold_Button_prob_mc2_mch \
	M3_Block_Timeslots_prob_mc2_mch \
	M4_Zoom_prob_mc2_mch \
	M5_AMAN_Timeout_prob_mc2_mch \
	M6_Select_Airplane_prob_mc2_mch \
	M7_Interaction_Pauses_Updates_prob_mc2_mch \
	M8_Interaction_Events_prob_mc2_mch \
	M9_Push_Mouse_Buttons_prob_mc2_mch
# These are expected to take longer than an hour, so we don't even try by default.
MACHINES_TIMEOUT := \
	M3_Block_Timeslots_prob_mc_mch \
	M4_Zoom_prob_mc_mch \
	M5_AMAN_Timeout_prob_mc_mch \
	M6_Select_Airplane_prob_mc_mch \
	M7_Interaction_Pauses_Updates_prob_mc_mch \
	M8_Interaction_Events_prob_mc_mch \
	M9_Push_Mouse_Buttons_prob_mc_mch
LOG_FILES := $(addsuffix .mc.log,$(MACHINES))

.PHONY: all
all: check_exist $(LOG_FILES)

.PHONY: check_exist
check_exist: $(addsuffix .eventb,$(MACHINES))
	@echo "Success: All required .eventb files are present."

TIME='time' # Quoted to ensure that it's always the command and not the shell builtin.
TIMEOUT=timeout
PROBCLI=probcli
FLAGS=--model-check -disable-time-out -p OPERATION_REUSE full -pref_group model_check unlimited -p COMPRESSION TRUE -noass -memory -p TIME_OUT 5000 -p MAX_OPERATIONS 100000 -p MAX_INITIALISATIONS 100000

%.mc.log: %.eventb
	echo "Checking $<..." > $@.temp.log
	for i in 1 2 3 4 5; do $(TIMEOUT) 60m $(TIME) -f "Run $$i: walltime %E sec, max RSS %M kB for %C" $(PROBCLI) $< $(FLAGS) 2>&1 | tee -a $@.temp.log; done
	mv $@.temp.log $@

model_check_results.log: $(LOG_FILES)
	awk '/^Checking .*\.\.\.$$/ {print ""; print "================"; print; print "================";}; /^% Model checking finished/ {do_print = 1;}; do_print; /^Run [0-9]+:/ {do_print = 0;}' $^ > $@

model_check_results.csv: model_check_results.log
	python3 collect_model_check_results.py $< $@

.PHONY: clean
clean:
	rm *.prob
