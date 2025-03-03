import math


class DFSExpenseShareAlgorithm:
    
    def __init__(self):
        self.TOTAL = 0
        
    def compute_net_balances(self, payments, owes):
        net = {}
        persons = set(payments.keys()) | set(owes.keys())
        for person in persons:
            net[person] = payments.get(person, 0) - owes.get(person, 0)
        return net

    def optimal_transactions(self, payments, owes):
        net = self.compute_net_balances(payments, owes)
        
        debtors = []
        creditors = []
        eps = 1e-8
        for person, balance in net.items():
            if balance < -eps:
                debtors.append((person, -balance))
            elif balance > eps:
                creditors.append((person, balance))

        best_transactions = None
        best_count = math.inf

        def dfs(current_debtors, current_creditors, transactions):
            nonlocal best_transactions, best_count
            
            if not current_debtors and not current_creditors:
                if len(transactions) < best_count:
                    best_count = len(transactions)
                    best_transactions = transactions.copy()
                return
            
            if len(transactions) >= best_count:
                return
            self.TOTAL += 1
            debtor, d_amt = current_debtors[0]
            for i in range(len(current_creditors)):
                creditor, c_amt = current_creditors[i]
                transfer = min(d_amt, c_amt)
                
                new_transactions = transactions + [(debtor, creditor, transfer)]
                
                new_debtors = current_debtors.copy()
                new_creditors = current_creditors.copy()
                
                if math.isclose(d_amt, transfer, rel_tol=1e-8) or d_amt < transfer:
                    new_debtors = new_debtors[1:]
                else:
                    new_debtors[0] = (debtor, d_amt - transfer)
                
                if math.isclose(c_amt, transfer, rel_tol=1e-8) or c_amt < transfer:
                    new_creditors.pop(i)
                else:
                    new_creditors[i] = (creditor, c_amt - transfer)
                
                dfs(new_debtors, new_creditors, new_transactions)
        
        dfs(debtors, creditors, [])
        return best_transactions if best_transactions is not None else []
    

class GreedyExpenseShareAlgorithm:
    def __init__(self):
        raise NotImplementedError("This class is not implemented and cannot be instantiated.")

# # Example usage:
# payments = {
#     "Alice": 30,
#     "Martin": 5,
#     "Bob": 5,
#     "Charlie": 0,
# }
# owes = {
#     "Alice": 0,
#     "Bob": 10,
#     "Charlie": 30,
    
# }

# alg = DFSExpenseShareAlgorithm()
# net_balances = alg.compute_net_balances(payments, owes)
# print("Net Balances:")
# for person, balance in net_balances.items():
#     print(f"  {person}: {balance:.2f}")

# transactions = alg.optimal_transactions(payments, owes)
# print("\nTransactions to settle up (debtor pays creditor):")
# for debtor, creditor, amount in transactions:
#     print(f"  {debtor} pays {creditor}: ${amount:.2f}")
# print(f"\nTotal transactions: {len(transactions)}")

