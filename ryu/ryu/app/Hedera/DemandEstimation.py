
from __future__ import print_function

def demand_estimation(flows, hostsList):
	"""
		Main function of demand estimation.
	"""
	M = {}
	for i in hostsList:
		M[i] = {}
		for j in hostsList:
			M[i][j] = {'demand': 0, 'pre_demand': 0, 'converged': False, 'FlowNumber': 0}

	for flow in flows:
		M[flow['src']][flow['dst']]['FlowNumber'] += 1

	demandChange = True
	while demandChange:
		demandChange = False
		for src in hostsList:
			estimate_src(M, flows, src)

		for dst in hostsList:
			estimate_dst(M, flows, dst)

		for i in hostsList:
			for j in hostsList:
				if M[i][j]['pre_demand'] != M[i][j]['demand']:
					demandChange = True
					M[i][j]['pre_demand'] = M[i][j]['demand']

	demandsPrinting(M, hostsList)
	return flows

def estimate_src(M, flows, src):
	"""
	Estimate and assign demands for flows from a given source.

	Behavior (scheme 1): keep measured demands when possible. Only when the
	sum of (converged + measured-unconverged) exceeds 1.0 do we scale the
	unconverged flows down proportionally to fit the remaining budget.
	"""
	converged_demand = 0.0
	unconverged = []
	for flow in flows:
		if flow['src'] == src:
			if flow.get('converged'):
				converged_demand += flow.get('demand', 0.0)
			else:
				unconverged.append(flow)

	if not unconverged:
		return

	# Sum of current (measured) demands for unconverged flows
	sum_unconv = sum(f.get('demand', 0.0) for f in unconverged)

	# If no measured demand available (all zeros), fall back to equal share
	if sum_unconv == 0.0:
		equal_share = max((1.0 - converged_demand) / len(unconverged), 0.0)
		for f in unconverged:
			M[f['src']][f['dst']]['demand'] = equal_share
			f['demand'] = equal_share
		return

	# If current measured sum fits within remaining budget, keep measurements
	if converged_demand + sum_unconv <= 1.0:
		for f in unconverged:
			# ensure stored value present in M as well
			M[f['src']][f['dst']]['demand'] = f.get('demand', 0.0)
			# keep flow['demand'] unchanged
		return

	# Otherwise scale unconverged measured demands down proportionally
	remaining = max(1.0 - converged_demand, 0.0)
	scale = remaining / sum_unconv if sum_unconv > 0 else 0.0
	for f in unconverged:
		newd = f.get('demand', 0.0) * scale
		M[f['src']][f['dst']]['demand'] = newd
		f['demand'] = newd

def estimate_dst(M, flows, dst):
	total_demand = 0
	sender_limited_demand = 0
	receiver_limited_num = 0
	for flow in flows:
		if flow['dst'] == dst:
			flow['receiver_limited'] = True
			total_demand += flow['demand']
			receiver_limited_num += 1

	if total_demand <= 1.0:
		return
	else:
		equal_share = 1.0 / receiver_limited_num
		flagFlip=True
		while flagFlip:
			flagFlip = False
			receiver_limited_num = 0
			for flow in flows:
				if flow['dst'] == dst and flow['receiver_limited']:
					if flow['demand'] < equal_share:
						sender_limited_demand += flow['demand']
						flow['receiver_limited'] = False
						flagFlip = True
					else:
						receiver_limited_num += 1
			equal_share = (1.0 - sender_limited_demand) / receiver_limited_num

		for flow in flows:
			if flow['dst'] == dst and flow['receiver_limited']:
				M[flow['src']][flow['dst']]['demand'] = equal_share
				M[flow['src']][flow['dst']]['converged'] = True
				flow['converged'] = True
				flow['demand'] = equal_share

def demandsPrinting(M, hostsList):
	"""
		Show the estimate results.
	"""
	print("********************Estimated Demands********************")
	print()
	for host in hostsList:
		print(host, end=' ')
	print()
	print('_' * 140)
	for row in hostsList:
		print(row, end=' | ')
		for col in hostsList:
			print('%.2f' % M[row][col]['demand'], end=' ')
		print()
	print()
