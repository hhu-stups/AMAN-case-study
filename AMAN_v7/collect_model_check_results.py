#!/usr/bin/env python3


import csv
import re
import statistics
import sys


def process_model(model_name, log_stream, csv_writer):
	all_mc_time_ms = []
	all_mc_walltime_ms = []
	last_states = None
	last_transitions = None
	all_prob_mem_mb = []
	all_prob_program_mem_mb = []
	all_total_walltime = []
	all_max_rss_kb = []
	
	for line in log_stream:
		line = line.strip()
		if line.startswith("Checking "):
			next_model_name = line[len("Checking "):-len("...")]
			break
		elif line.startswith("Model checking time: "):
			match = re.match(r"^Model checking time: ([0-9]+) ms \(([0-9]+) ms walltime\)", line)
			mc_time_ms = int(match.group(1))
			mc_walltime_ms = int(match.group(2))
		elif line.startswith("States analysed: "):
			states = int(line[len("States analysed: "):])
		elif line.startswith("Transitions fired: "):
			transitions = int(line[len("Transitions fired: "):])
		elif line.startswith("ProB memory used: "):
			match = re.match(r"^ProB memory used: *([0-9.]+) MB \( *([0-9.]+) MB program\)", line)
			prob_mem_mb = float(match.group(1))
			prob_program_mem_mb = float(match.group(2))
		elif line.startswith("Run "):
			match = re.match(r"^Run ([0-9]+): walltime ([0-9]+):([0-9.]+) sec, max RSS ([0-9]+) kB", line)
			run_number = int(match.group(1))
			total_walltime = int(match.group(2)) * 60 + float(match.group(3))
			max_rss_kb = int(match.group(4))
			
			if last_states is not None and last_states != states:
				print(f"Warning: Runs {last_run_number} and {run_number} for {model_name!r} explored a different number of states: {last_states} != {states}", file=sys.stderr)
			
			if last_transitions is not None and last_transitions != transitions:
				print(f"Warning: Runs {last_run_number} and {run_number} for {model_name!r} explored a different number of transitions: {last_transitions} != {transitions}", file=sys.stderr)
			
			# noinspection PyUnboundLocalVariable
			csv_writer.writerow([model_name, run_number, mc_time_ms, mc_walltime_ms, states, transitions, prob_mem_mb, prob_program_mem_mb, total_walltime, max_rss_kb])
			
			all_mc_time_ms.append(mc_time_ms)
			all_mc_walltime_ms.append(mc_walltime_ms)
			all_prob_mem_mb.append(prob_mem_mb)
			all_prob_program_mem_mb.append(prob_program_mem_mb)
			all_total_walltime.append(total_walltime)
			all_max_rss_kb.append(max_rss_kb)
			
			last_run_number = run_number
			last_states = states
			last_transitions = transitions
			# Force an error if any of these values are missing in the next check's log.
			del run_number, mc_time_ms, mc_walltime_ms, states, transitions, prob_mem_mb, prob_program_mem_mb, total_walltime, max_rss_kb
	else:
		next_model_name = None
	
	return all_mc_time_ms, all_mc_walltime_ms, last_states, last_transitions, all_prob_mem_mb, all_prob_program_mem_mb, all_total_walltime, all_max_rss_kb, next_model_name


def process_log(log_stream, csv_writer):
	csv_writer.writerow(["Name", "Run", "ProB time (ms)", "ProB walltime (ms)", "States", "Transitions", "ProB memory (MB)", "ProB program memory (MB)", "Total walltime (sec)", "Max RSS (kB)"])
	
	*_, model_name = process_model(None, log_stream, csv_writer)
	while model_name is not None:
		all_mc_time_ms, all_mc_walltime_ms, states, transitions, all_prob_mem_mb, all_prob_program_mem_mb, all_total_walltime, all_max_rss_kb, next_model_name = process_model(model_name, log_stream, csv_writer)
		
		csv_writer.writerow([model_name, "Median", statistics.median(all_mc_time_ms), statistics.median(all_mc_walltime_ms), states, transitions, statistics.median(all_prob_mem_mb), statistics.median(all_prob_program_mem_mb), statistics.median(all_total_walltime), statistics.median(all_max_rss_kb)])
		
		model_name = next_model_name


def main():
	if len(sys.argv) != 3:
		print(f"usage: {sys.argv[0]} INPUT_LOG_FILE OUTPUT_CSV_FILE")
	
	_, log_name, csv_name = sys.argv
	with open(log_name, "r", encoding="utf-8") as fin:
		with open(csv_name, "w", encoding="utf-8", newline="") as fout:
			csv_writer = csv.writer(fout)
			process_log(fin, csv_writer)
	
	sys.exit(0)


if __name__ == "__main__":
	sys.exit(main())
