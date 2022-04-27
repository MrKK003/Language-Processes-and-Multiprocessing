import codecs
import sys

class DFA:
    
    def __init__(self,filepath):
        self.InputFile = codecs.open(filepath, "r+", "utf-8")
        self.S = self.populate_states()
        self.A = self.populate_alphabet()
        self.f_SxA = self.populate_transition_function()
        self.s_0, self.P_S = self.set_start_accept()
        self.c_state = None

    def set_start_accept(self):
        line = self.InputFile.readline().split()
        start = line[1]
        accept = line[3:]
        if (start in self.S) and (set(accept).issubset(set(self.S))):
            return start, accept

    def populate_states(self):
        line = self.InputFile.readline().split()
        S_input = line[1:]
        print("Стани : {}".format(S_input))
        return S_input

    def populate_alphabet(self):
        line = self.InputFile.readline().split()
        A_input = line[1:]
        print("Абетка : {}".format(A_input))
        return A_input

    def populate_transition_function(self):
        transition_dict = {el : {el_2 : 'REJECT' for el_2 in self.A} for el in self.S}
        for key, dict_value in transition_dict.items():
            line = self.InputFile.readline().split()
            i=1
            for input_alphabet, transition_state in dict_value.items():
                transition_dict[key][input_alphabet] = line[i]
                i+=1
        print("\nФункція переходів: f: SxA->P(S)")
        print("Теперішній стан\tВхідний символ\tНаступний стан")
        for key, dict_value in transition_dict.items():
            for input_alphabet, transition_state in dict_value.items():
                print("{}\t\t{}\t\t{}".format(key, input_alphabet, transition_state))
        print('\n')
        return transition_dict

    def run_state_transition(self, input_symbol):
        if (self.c_state == 'REJECT'):
            return False
        print("Теперішній стан {}\tВхідний символ : {}\t Наступний стан : {}".format(self.c_state, input_symbol, self.f_SxA[self.c_state][input_symbol]))
        self.c_state = self.f_SxA[self.c_state][input_symbol]
        return self.c_state

    def check_if_accept(self):
        if self.c_state in self.P_S:
            return True
        else:
            return False

    def accepts(self,s):
        state = self.s_0
        for c in s:
            if not(c in self.A):
                return False
            state = self.f_SxA[state][c]
        return state in self.P_S

    def Diff(self,li1, li2): 
        return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1)))) 

    def minimize(self):
        P = [set(self.P_S),self.Diff(self.S,self.P_S)]
        W = [set(self.P_S)]

        while len(W) != 0:
            A = W[0]
            W.remove(A)
            X = set()
            for c in self.A:
                for from_state, to_state in self.f_SxA.items():
                    for toNum, value in to_state.items():
                        if c in value and toNum in A:
                            X.update(set([from_state]))
            for Y in P:
                if not X.intersection(Y) == set():
                    P.append(X.intersection(Y))
                    P.append(Y.difference(X))
                    if Y in W:
                        W.append(X.intersection(Y))
                        W.append(Y.difference(X))
                        W.remove(Y)
                    else :
                        if len(X.intersection(Y)) <= len (Y.difference(X)):
                            W.append(X.intersection(Y))
                            #W.remove(Y)
                        else :
                            W.append(Y.difference(X))
                            #W.remove(Y)
                    P.remove(Y)
        return P,W

if __name__ == "__main__":
    try:
        A1 = DFA("/Applications/ТПМП/A1.txt") #your location
    except:
        print("No arguments were given")
    print("(P,W) = ",A1.minimize())