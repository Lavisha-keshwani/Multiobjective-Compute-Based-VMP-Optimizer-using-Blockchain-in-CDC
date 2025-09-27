import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize

class CloudProblem(ElementwiseProblem):
    def __init__(self, n_vms=10, n_hosts=5):
        super().__init__(n_var=n_vms, n_obj=2, n_constr=1, xl=0, xu=n_hosts-1, type_var=int)
        self.n_vms = n_vms
        self.n_hosts = n_hosts
        # Generate random workload for testing
        self.vm_loads = np.random.randint(10, 100, size=n_vms)
        self.host_capacity = np.full(n_hosts, 200)
        self.host_power = np.random.randint(100, 200, size=n_hosts)

    def _evaluate(self, x, out, *args, **kwargs):
        host_usage = np.zeros(self.n_hosts)
        for vm, host in enumerate(x):
            host = int(round(host))
            host_usage[host] += self.vm_loads[vm]

        # Calculate energy consumption
        active_hosts = host_usage > 0
        energy = np.sum(self.host_power[active_hosts])

        # Calculate SLA violations
        sla_violation = np.sum(host_usage > self.host_capacity)

        # Constraint: max 20% hosts can be overloaded
        g1 = sla_violation - (0.2 * self.n_hosts)

        out["F"] = [energy, sla_violation]
        out["G"] = [g1]

def run_optimization():
    # Create results directory
    os.makedirs("results", exist_ok=True)

    # Setup and run optimization
    problem = CloudProblem(n_vms=12, n_hosts=6)
    algorithm = NSGA2(
        pop_size=20,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

    res = minimize(problem, algorithm, ('n_gen', 30), verbose=True)

    # Save results
    df = pd.DataFrame(res.F, columns=["Energy", "SLA"])
    df.to_csv("results/results.csv", index=False)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.scatter(res.F[:, 0], res.F[:, 1], c="blue", marker="o")
    plt.xlabel("Energy Consumption")
    plt.ylabel("SLA Violations")
    plt.title("Pareto Front: Energy vs SLA")
    plt.grid(True)
    plt.savefig("results/pareto_front.png")
    plt.close()

    print("✅ Optimization complete!")
    print("Results saved in results/results.csv")
    print("Plot saved in results/pareto_front.png")

if __name__ == "__main__":
    run_optimization()
# #         xu = np.full(n_var, len(hosts)-1, dtype=int)
# #         super().__init__(n_var=n_var, n_obj=3, n_constr=0, xl=xl, xu=xu, elementwise=True)

# #     def _evaluate(self, x, out, *args, **kwargs):
# #         hosts = self.hosts; vms = self.vms; T = self.T_hours
# #         host_cpu_used = np.zeros(len(hosts)); host_ram_used = np.zeros(len(hosts))
# #         for i,hi in enumerate(x):
# #             vm = vms[i]; host_cpu_used[hi] += vm['mips']; host_ram_used[hi] += vm['ram']
# #         energy = 0.0; carbon = 0.0; sla_penalty = 0.0
# #         for i,h in enumerate(hosts):
# #             cpu_cap = h['cpu_mips']; ram_cap = h['ram_mb']
# #             util = min(1.0, host_cpu_used[i]/cpu_cap) if cpu_cap>0 else 1.0
# #             p = h['p_idle'] + (h['p_max'] - h['p_idle']) * util
# #             E_h = p * T
# #             energy += E_h
# #             region = h.get('region','r0')
# #             ci = self.carbon_map.get(region, 400.0)
# #             carbon += (E_h/1000.0) * ci
# #             if host_cpu_used[i] > cpu_cap or host_ram_used[i] > ram_cap:
# #                 sla_penalty += 1e6
# #         out["F"] = np.array([energy, carbon, sla_penalty])

# # def nsga2_allocate(hosts, vms, carbon_map, pop_size=40, n_gen=20):
# #     if len(vms) > 30:
# #         return greedy_mbfd(hosts, vms)
# #     prob = VMPlacementProblem(hosts, vms, carbon_map, T_hours=1.0)
# #     algo = NSGA2(
# #         pop_size=pop_size,
# #         sampling=IntegerRandomSampling(),
# #         crossover=SBX(prob=0.9, eta=15),
# #         mutation=PM(eta=20)
# #     )
# #     res = minimize(prob, algo, ('n_gen', n_gen), verbose=False)
# #     # pick solution minimizing carbon with SLA_penalty == 0 if possible
# #     F = res.F; X = res.X
# #     if F.shape[0] == 0:
# #         return greedy_mbfd(hosts, vms)
# #     # prefer solutions with sla_penalty small
# #     feasible_idx = [i for i in range(len(F)) if F[i,2] < 1e5]
# #     if feasible_idx:
# #         best = min(feasible_idx, key=lambda i: F[i,1])
# #     else:
# #         best = int(np.argmin(F[:,1]))
# #     return [int(v) for v in X[best]]

# # # ------------------ Simulation & metrics ------------------
# # def compute_metrics_from_mapping(hosts, vms, mapping, carbon_map):
# #     host_cpu_used = [0]*len(hosts); host_ram_used=[0]*len(hosts)
# #     for i,hid in enumerate(mapping):
# #         host_cpu_used[hid] += vms[i]['mips']; host_ram_used[hid] += vms[i]['ram']
# #     total_energy_wh = 0.0; total_carbon_g = 0.0
# #     sla_violations = 0
# #     for i,h in enumerate(hosts):
# #         cpu_cap = h['cpu_mips']; ram_cap = h['ram_mb']
# #         util = min(1.0, host_cpu_used[i]/cpu_cap) if cpu_cap>0 else 1.0
# #         p = h['p_idle'] + (h['p_max'] - h['p_idle'])*util
# #         E = p * 1.0
# #         total_energy_wh += E
# #         ci = carbon_map.get(h.get('region','r0'), 400.0)
# #         total_carbon_g += (E/1000.0)*ci
# #         if host_cpu_used[i] > cpu_cap or host_ram_used[i] > ram_cap:
# #             sla_violations += 1
# #     # throughput proxy: sum of VM mips (normalized)
# #     throughput = sum([vm['mips'] for vm in vms])
# #     return total_energy_wh, total_carbon_g, throughput, sla_violations

# # # ------------------ main runner ------------------
# # def main():
# #     os.makedirs("results", exist_ok=True)
# #     # Start Prometheus metrics server on 8000
# #     start_http_server(8000)
# #     g_energy = Gauge('sim_energy_wh', 'Energy Wh', ['scenario'])
# #     g_carbon = Gauge('sim_carbon_g', 'Carbon g', ['scenario'])
# #     g_through = Gauge('sim_throughput', 'Throughput proxy', ['scenario'])
# #     g_sla = Gauge('sim_sla_viol', 'SLA violations', ['scenario'])
# #     c_place = Counter('placement_requests_total', 'placement requests', ['method'])

# #     # deploy local blockchain contract
# #     w3, contract, acct = deploy_contract()

# #     # Define a small dc (3 hosts)
# #     hosts = [
# #         {'id':0,'cpu_mips':8000,'ram_mb':32768,'p_idle':80.0,'p_max':200.0,'region':'r0'},
# #         {'id':1,'cpu_mips':12000,'ram_mb':65536,'p_idle':100.0,'p_max':300.0,'region':'r1'},
# #         {'id':2,'cpu_mips':16000,'ram_mb':131072,'p_idle':120.0,'p_max':350.0,'region':'r0'}
# #     ]

# #     # VM templates (we will scale load by multiplying mips)
# #     base_vms = [{'mips':1000,'ram':2048} for _ in range(8)]  # 8 small VMs

# #     loads = [20,40,60,80,100]  # percent (affects mips scaling)
# #     carbon_profiles = {'low':200.0, 'high':600.0}
# #     rows = []
# #     for profile_name, ci in carbon_profiles.items():
# #         carbon_map = {'r0':ci, 'r1':ci}
# #         for load in loads:
# #             # scale mips proportional to load
# #             scale = load/100.0
# #             vms = []
# #             for vm in base_vms:
# #                 vms.append({'mips': max(100, int(vm['mips']*scale)), 'ram': vm['ram']})
# #             # Baseline: greedy
# #             mapping_base = greedy_mbfd(hosts, vms)
# #             E_b, C_b, T_b, S_b = compute_metrics_from_mapping(hosts, vms, mapping_base, carbon_map)
# #             c_place.labels(method='greedy').inc()
# #             # Proposed: NSGA2
# #             mapping_prop = nsga2_allocate(hosts, vms, carbon_map, pop_size=30, n_gen=16)
# #             c_place.labels(method='nsga2').inc()
# #             E_p, C_p, T_p, S_p = compute_metrics_from_mapping(hosts, vms, mapping_prop, carbon_map)
# #             # Write to blockchain (log proposed mapping)
# #             try:
# #                 tx = contract.functions.logPlacement(
# #                     [i for i in range(len(vms))],
# #                     mapping_prop,
# #                     int(E_p),
# #                     int(C_p)
# #                 ).transact({'from': acct})
# #                 # eth-tester auto-mines; we can wait but it's instant
# #             except Exception as e:
# #                 print("Blockchain log failed:", e)

# #             # Update prometheus
# #             scen = f"{profile_name}_{load}"
# #             g_energy.labels(scenario=scen).set(E_p)
# #             g_carbon.labels(scenario=scen).set(C_p)
# #             g_through.labels(scenario=scen).set(T_p)
# #             g_sla.labels(scenario=scen).set(S_p)

# #             # Save CSV row (baseline & proposed)
# #             rows.append({
# #                 'profile':profile_name, 'load_pct':load,
# #                 'method':'baseline','energy_wh':E_b,'carbon_g':C_b,'throughput':T_b,'sla_viol':S_b
# #             })
# #             rows.append({
# #                 'profile':profile_name, 'load_pct':load,
# #                 'method':'proposed','energy_wh':E_p,'carbon_g':C_p,'throughput':T_p,'sla_viol':S_p
# #             })
# #             print(f"Profile {profile_name} Load {load}% => baseline E={E_b:.1f}Wh C={C_b:.1f}g | proposed E={E_p:.1f}Wh C={C_p:.1f}g")
# #             time.sleep(0.2)  # small pause so prometheus can scrape if running

# #     # Save CSV
# #     df = pd.DataFrame(rows)
# #     df.to_csv("results/results.csv", index=False)
# #     print("Saved results/results.csv")

# #     # Plotting: 4 graphs
# #     # 1) carbon vs load for profile high & low
# #     for profile in carbon_profiles.keys():
# #         dfp = df[df.profile==profile]
# #         fig, ax = plt.subplots()
# #         for method in ['baseline','proposed']:
# #             dsub = dfp[dfp.method==method]
# #             ax.plot(dsub.load_pct, dsub.carbon_g/1000.0, marker='o', label=method) # kg
# #         ax.set_xlabel("Load %"); ax.set_ylabel("Carbon (kg)"); ax.set_title(f"Carbon vs Load ({profile})")
# #         ax.legend(); fig.savefig(f"results/carbon_vs_load_{profile}.png")

# #     # 2) Energy vs load (kWh)
# #     for profile in carbon_profiles.keys():
# #         dfp = df[df.profile==profile]
# #         fig, ax = plt.subplots()
# #         for method in ['baseline','proposed']:
# #             dsub = dfp[dfp.method==method]
# #             ax.plot(dsub.load_pct, dsub.energy_wh/1000.0, marker='o', label=method)
# #         ax.set_xlabel("Load %"); ax.set_ylabel("Energy (kWh)"); ax.set_title(f"Energy vs Load ({profile})")
# #         ax.legend(); fig.savefig(f"results/energy_vs_load_{profile}.png")

# #     # 3) Throughput vs load
# #     for profile in carbon_profiles.keys():
# #         dfp = df[df.profile==profile]
# #         fig, ax = plt.subplots()
# #         for method in ['baseline','proposed']:
# #             dsub = dfp[dfp.method==method]
# #             ax.plot(dsub.load_pct, dsub.throughput, marker='o', label=method)
# #         ax.set_xlabel("Load %"); ax.set_ylabel("Throughput (proxy)"); ax.set_title(f"Throughput vs Load ({profile})")
# #         ax.legend(); fig.savefig(f"results/throughput_vs_load_{profile}.png")

# #     # 4) Energy efficiency (throughput per kWh) bar (aggregated)
# #     agg = df.groupby(['method']).agg({'throughput':'mean','energy_wh':'mean'}).reset_index()
# #     agg['ops_per_kwh'] = agg['throughput'] / (agg['energy_wh']/1000.0)
# #     fig, ax = plt.subplots()
# #     ax.bar(agg['method'], agg['ops_per_kwh'])
# #     ax.set_ylabel("Ops/sec per kWh"); ax.set_title("Energy efficiency")
# #     fig.savefig("results/energy_efficiency_bar.png")

# #     print("Plots saved in results/*.png")
# #     print("Simulation complete. Open Grafana (http://localhost:3000) to view scraped metrics (if monitoring stack up).")

# # if __name__ == "__main__":
# #     main()


# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from pymoo.core.problem import ElementwiseProblem
# from pymoo.algorithms.moo.nsga2 import NSGA2
# from pymoo.operators.sampling.rnd import IntegerRandomSampling
# from pymoo.operators.crossover.sbx import SBX
# from pymoo.operators.mutation.pm import PM
# from pymoo.optimize import minimize
# import os

# # -------------------------------
# # Cloud Simulation Problem
# # -------------------------------
# class CloudProblem(ElementwiseProblem):
#     def __init__(self, n_vms=10, n_hosts=5):
#         super().__init__(n_var=n_vms, n_obj=2, n_constr=1, xl=0, xu=n_hosts-1, type_var=int)
#         self.n_vms = n_vms
#         self.n_hosts = n_hosts
#         self.vm_loads = np.random.randint(10, 100, size=n_vms)  # VM loads
#         self.host_capacity = np.full(n_hosts, 200)              # Host capacities
#         self.host_power = np.random.randint(100, 200, size=n_hosts)  # Host power use

#     def _evaluate(self, x, out, *args, **kwargs):
#         host_usage = np.zeros(self.n_hosts)
#         for vm, host in enumerate(x):
#             host = int(round(host))   # convert to int
#             host_usage[host] += self.vm_loads[vm]

#         # Objective 1: Energy
#         active_hosts = host_usage > 0
#         energy = np.sum(self.host_power[active_hosts])

#         # Objective 2: SLA violations
#         sla_violation = np.sum(host_usage > self.host_capacity)

#         # Constraint
#         g1 = sla_violation - (0.2 * self.n_hosts)

#         out["F"] = [energy, sla_violation]
#         out["G"] = [g1]

# # -------------------------------
# # Run Optimization
# # -------------------------------
# def run_experiment():
#     problem = CloudProblem(n_vms=15, n_hosts=6)

#     algo = NSGA2(
#         pop_size=20,
#         sampling=IntegerRandomSampling(),
#         crossover=SBX(prob=0.9, eta=15),
#         mutation=PM(eta=20),
#         eliminate_duplicates=True
#     )

#     res = minimize(problem, algo, ('n_gen', 40), verbose=True)

#     return res

# # -------------------------------
# # Save Results
# # -------------------------------
# def save_results(res):
#     os.makedirs("results", exist_ok=True)
#     df = pd.DataFrame(res.F, columns=["Energy", "SLA"])
#     df.to_csv("results/results.csv", index=False)

#     # Plot Energy vs SLA
#     plt.scatter(res.F[:, 0], res.F[:, 1], c="blue", marker="o")
#     plt.xlabel("Energy Consumption")
#     plt.ylabel("SLA Violations")
#     plt.title("Pareto Front: Energy vs SLA")
#     plt.grid(True)
#     plt.savefig("results/pareto_front.png")
#     plt.close()

#     print("✅ Results saved in results/ folder")

# # -------------------------------
# # Main
# # -------------------------------
# if __name__ == "__main__":
#     res = run_experiment()
#     save_results(res)


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# pymoo (optimizer)
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize

# blockchain
from web3 import Web3
from eth_tester import EthereumTester
from solcx import compile_source, install_solc

install_solc("0.8.0")   # install solidity compiler


# -------------------------------
# Blockchain Setup
# -------------------------------
eth_tester = EthereumTester()
w3 = Web3(Web3.EthereumTesterProvider(eth_tester))
account = w3.eth.accounts[0]

# Solidity contract
contract_source = """
pragma solidity ^0.8.0;

contract PlacementLog {
    event PlacementSaved(uint indexed vm, uint indexed host);

    function savePlacement(uint vm, uint host) public {
        emit PlacementSaved(vm, host);
    }
}
"""

compiled_sol = compile_source(contract_source, solc_version="0.8.0")
contract_id, contract_interface = compiled_sol.popitem()
PlacementLog = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Deploy
tx_hash = PlacementLog.constructor().transact({'from': account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=contract_interface['abi'])

print("✅ Blockchain contract deployed at:", contract.address)


# -------------------------------
# Cloud Optimization Problem
# -------------------------------
class CloudProblem(ElementwiseProblem):
    def __init__(self, n_vms=10, n_hosts=5):
        super().__init__(n_var=n_vms, n_obj=2, n_constr=1, xl=0, xu=n_hosts-1, type_var=int)
        self.n_vms = n_vms
        self.n_hosts = n_hosts
        self.vm_loads = np.random.randint(10, 100, size=n_vms)
        self.host_capacity = np.full(n_hosts, 200)
        self.host_power = np.random.randint(100, 200, size=n_hosts)

    def _evaluate(self, x, out, *args, **kwargs):
        host_usage = np.zeros(self.n_hosts)
        for vm, host in enumerate(x):
            host = int(round(host))
            host_usage[host] += self.vm_loads[vm]
            # log to blockchain
            contract.functions.savePlacement(vm, host).transact({'from': account})

        # Objective 1: Energy
        active_hosts = host_usage > 0
        energy = np.sum(self.host_power[active_hosts])

        # Objective 2: SLA violations
        sla_violation = np.sum(host_usage > self.host_capacity)

        # Constraint: max 20% hosts overloaded
        g1 = sla_violation - (0.2 * self.n_hosts)

        out["F"] = [energy, sla_violation]
        out["G"] = [g1]


# -------------------------------
# Run Optimization
# -------------------------------
def run_experiment():
    problem = CloudProblem(n_vms=12, n_hosts=6)

    algo = NSGA2(
        pop_size=20,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=0.9, eta=15),
        mutation=PM(eta=20),
        eliminate_duplicates=True
    )

    res = minimize(problem, algo, ('n_gen', 30), verbose=True)
    return res


# -------------------------------
# Save & Plot Results
# -------------------------------
def save_results(res):
    os.makedirs("results", exist_ok=True)
    df = pd.DataFrame(res.F, columns=["Energy", "SLA"])
    df.to_csv("results/results.csv", index=False)

    # Pareto front
    plt.figure()
    plt.scatter(res.F[:, 0], res.F[:, 1], c="blue", marker="o")
    plt.xlabel("Energy Consumption")
    plt.ylabel("SLA Violations")
    plt.title("Pareto Front: Energy vs SLA")
    plt.grid(True)
    plt.savefig("results/pareto_front.png")
    plt.close()

    # Energy histogram
    plt.hist(res.F[:, 0], bins=10, color="green")
    plt.xlabel("Energy Consumption")
    plt.ylabel("Frequency")
    plt.title("Energy Distribution")
    plt.savefig("results/energy_hist.png")
    plt.close()

    # SLA histogram
    plt.hist(res.F[:, 1], bins=10, color="red")
    plt.xlabel("SLA Violations")
    plt.ylabel("Frequency")
    plt.title("SLA Distribution")
    plt.savefig("results/sla_hist.png")
    plt.close()

    print("✅ Results saved in results/ folder")


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    res = run_experiment()
    save_results(res)
