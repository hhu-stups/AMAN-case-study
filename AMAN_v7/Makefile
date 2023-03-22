.SUFFIXES:

.PHONY: all clean

all: M0_AMAN_Update_prob_mc_mch M1_Landing_Sequence_prob_mc_mch M2_Hold_Button_prob_mc_mch M3_Block_Timeslots_prob_mc_mch M4_Zoom_prob_mc_mch M5_AMAN_Timeout_prob_mc_mch M6_Select_Airplane_prob_mc_mch M7_Interaction_Pauses_Updates_prob_mc_mch M8_Interaction_Events_prob_mc_mch M9_Push_Mouse_Buttons_prob_mc_mch M10_GUI_prob_mc_mch M0_AMAN_Update_prob_mc2_mch M1_Landing_Sequence_prob_mc2_mch M2_Hold_Button_prob_mc2_mch M3_Block_Timeslots_prob_mc2_mch M4_Zoom_prob_mc2_mch M5_AMAN_Timeout_prob_mc2_mch M6_Select_Airplane_prob_mc2_mch M7_Interaction_Pauses_Updates_prob_mc2_mch M8_Interaction_Events_prob_mc2_mch M9_Push_Mouse_Buttons_prob_mc2_mch M10_GUI_prob_mc2_mch

PROBCLI=./probcli.sh
FLAGS=--model-check -disable-time-out -p OPERATION_REUSE full -pref_group model_check unlimited -p COMPRESSION TRUE -noass -memory -p TIME_OUT 5000 -p MAX_OPERATIONS 100000 -p MAX_INITIALISATIONS 100000

OUTPUT ?= runtimes.txt

% :
	timeout 60m gtime -f "%C %E %M" -ao $(OUTPUT) $(PROBCLI) $@.eventb $(FLAGS)
	timeout 60m gtime -f "%C %E %M" -ao $(OUTPUT) $(PROBCLI) $@.eventb $(FLAGS)
	timeout 60m gtime -f "%C %E %M" -ao $(OUTPUT) $(PROBCLI) $@.eventb $(FLAGS)
	timeout 60m gtime -f "%C %E %M" -ao $(OUTPUT) $(PROBCLI) $@.eventb $(FLAGS)
	timeout 60m gtime -f "%C %E %M" -ao $(OUTPUT) $(PROBCLI) $@.eventb $(FLAGS)

clean:
	rm *.prob
