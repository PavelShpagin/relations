from collections import defaultdict, deque
import shlex


class Ontology:
    def __init__(self):
        self.classes = set()
        self.instances = set()
        self.instance_of = {}
        self.rels = {
            "is_a": defaultdict(set),
            "part_of": defaultdict(set),
            "depends_on": defaultdict(set),
        }

    def add_class(self, c):
        self.classes.add(c)

    def add_is_a(self, child, parent):
        self.add_class(child)
        self.add_class(parent)
        self.rels["is_a"][child].add(parent)

    def add_part_of(self, part, whole):
        self.add_class(part)
        self.add_class(whole)
        self.rels["part_of"][part].add(whole)

    def add_depends_on(self, a, b):
        self.add_class(a)
        self.add_class(b)
        self.rels["depends_on"][a].add(b)

    def add_instance(self, inst, clazz):
        self.add_class(clazz)
        self.instances.add(inst)
        self.instance_of[inst] = clazz

    def _reachable(self, start, target, relname):
        seen, stack = set(), [start]
        while stack:
            x = stack.pop()
            if x == target:
                return True
            if x in seen:
                continue
            seen.add(x)
            for y in self.rels[relname].get(x, ()):  # type: ignore[index]
                stack.append(y)
        return False

    def is_a(self, child, parent):
        return self._reachable(child, parent, "is_a")

    def part_of(self, part, whole):
        # Support entities (instances) by first trying direct edges, then lifting to classes
        if self._reachable(part, whole, "part_of"):
            return True
        # Lift instances to their classes
        a = self.instance_of.get(part, part) if part in self.instances else part
        b = self.instance_of.get(whole, whole) if whole in self.instances else whole
        return self._reachable(a, b, "part_of")

    def depends_on(self, a, b):
        return self._reachable(a, b, "depends_on")

    def any_path(self, a, b):
        q = deque([(a, None)])
        prev = {a: (None, None)}
        while q:
            x, _ = q.popleft()
            if x == b:
                path = []
                cur = b
                while prev[cur][0] is not None:
                    pnode, prel = prev[cur]
                    path.append((pnode, prel, cur))
                    cur = pnode  # type: ignore[assignment]
                path.reverse()
                return path
            for relname, graph in self.rels.items():
                for y in graph.get(x, ()):  # type: ignore[attr-defined]
                    if y not in prev:
                        prev[y] = (x, relname)
                        q.append((y, relname))
        return None

    def subclasses(self, c):
        return {x for x, parents in self.rels["is_a"].items() if c in parents}

    def is_leaf_class(self, c):
        return len(self.subclasses(c)) == 0

    def instances_of(self, c):
        return [i for i, cls in self.instance_of.items() if cls == c]

    def class_of(self, inst):
        return self.instance_of.get(inst)

    def is_class(self, x):
        return x in self.classes

    def is_instance(self, x):
        return x in self.instances

    def max_depth_from(self, root="Computer Science"):
        down = defaultdict(set)
        for child, parents in self.rels["is_a"].items():
            for p in parents:
                down[p].add(child)
        if root not in self.classes:
            return 0
        best = 0
        stack = [(root, 1)]
        while stack:
            node, d = stack.pop()
            best = max(best, d)
            for ch in down.get(node, ()):  # type: ignore[attr-defined]
                stack.append((ch, d + 1))
        return best

    def validate(self):
        assert len(self.classes) >= 20, f"Need ≥20 classes, have {len(self.classes)}"
        assert self.max_depth_from("Computer Science") >= 4, "Need an is_a chain of depth ≥4"
        leaves = [c for c in self.classes if self.is_leaf_class(c)]
        for c in leaves:
            if len(self.instances_of(c)) < 2:
                raise AssertionError(f'Leaf "{c}" must have ≥2 instances (has {len(self.instances_of(c))})')
        return True


def load_ontology():
    O = Ontology()

    # is_a taxonomy
    O.add_is_a("Theory of Computation", "Computer Science")
    O.add_is_a("Automata & Formal Languages", "Theory of Computation")
    O.add_is_a("Finite Automata", "Automata & Formal Languages")
    O.add_is_a("Context-Free Grammars", "Automata & Formal Languages")
    O.add_is_a("Complexity Theory", "Theory of Computation")
    O.add_is_a("Complexity Classes", "Complexity Theory")

    O.add_is_a("Programming Languages & Compilers", "Computer Science")
    O.add_is_a("Programming Paradigms", "Programming Languages & Compilers")
    O.add_is_a("Functional Programming", "Programming Paradigms")
    O.add_is_a("Object-Oriented Programming", "Programming Paradigms")
    O.add_is_a("Compilers", "Programming Languages & Compilers")
    O.add_is_a("Lexical Analysis", "Compilers")
    O.add_is_a("Parsing", "Compilers")

    O.add_is_a("Algorithms", "Computer Science")
    O.add_is_a("Graph Algorithms", "Algorithms")
    O.add_is_a("Shortest Path", "Graph Algorithms")
    O.add_is_a("Spanning Tree", "Graph Algorithms")
    O.add_is_a("Sorting", "Algorithms")

    O.add_is_a("Data Structures", "Computer Science")
    O.add_is_a("Trees", "Data Structures")
    O.add_is_a("Binary Search Tree", "Trees")
    O.add_is_a("Hashing", "Data Structures")
    O.add_is_a("Hash Table", "Hashing")
    O.add_is_a("Priority Queue", "Data Structures")

    O.add_is_a("Operating Systems", "Computer Science")
    O.add_is_a("Process Management", "Operating Systems")
    O.add_is_a("CPU Scheduling", "Process Management")
    O.add_is_a("Memory Management", "Operating Systems")
    O.add_is_a("Virtual Memory", "Memory Management")

    O.add_is_a("Computer Architecture", "Computer Science")
    O.add_is_a("Instruction Set Architecture", "Computer Architecture")
    O.add_is_a("RISC", "Instruction Set Architecture")
    O.add_is_a("CISC", "Instruction Set Architecture")
    O.add_is_a("Parallel Models", "Computer Architecture")
    O.add_is_a("SIMD", "Parallel Models")
    O.add_is_a("MIMD", "Parallel Models")

    O.add_is_a("Computer Networks", "Computer Science")
    O.add_is_a("Protocol Stack", "Computer Networks")
    O.add_is_a("Transport Layer", "Protocol Stack")
    O.add_is_a("Network Layer", "Protocol Stack")

    O.add_is_a("Databases", "Computer Science")
    O.add_is_a("Relational Databases", "Databases")
    O.add_is_a("Key–Value Stores", "Databases")

    O.add_is_a("Cryptography", "Computer Science")
    O.add_is_a("Symmetric Cryptography", "Cryptography")
    O.add_is_a("Public-Key Cryptography", "Cryptography")

    O.add_is_a("Artificial Intelligence", "Computer Science")
    O.add_is_a("Machine Learning", "Artificial Intelligence")
    O.add_is_a("Supervised Learning", "Machine Learning")
    O.add_is_a("Unsupervised Learning", "Machine Learning")
    O.add_is_a("Natural Language Processing", "Artificial Intelligence")
    O.add_is_a("Language Modeling", "Natural Language Processing")

    O.add_is_a("Computational Geometry", "Computer Science")
    O.add_is_a("Planar Geometry", "Computational Geometry")
    O.add_is_a("Triangulation", "Planar Geometry")

    # part_of (composition)
    O.add_part_of("Lexical Analysis", "Compilers")
    O.add_part_of("Parsing", "Compilers")
    O.add_part_of("Process Management", "Operating Systems")
    O.add_part_of("CPU Scheduling", "Process Management")
    O.add_part_of("Memory Management", "Operating Systems")
    O.add_part_of("Virtual Memory", "Memory Management")
    O.add_part_of("Protocol Stack", "Computer Networks")
    O.add_part_of("Transport Layer", "Protocol Stack")
    O.add_part_of("Network Layer", "Protocol Stack")
    O.add_part_of("Instruction Set Architecture", "Computer Architecture")
    O.add_part_of("Parallel Models", "Computer Architecture")

    # depends_on (prerequisites)
    O.add_depends_on("Lexical Analysis", "Finite Automata")
    O.add_depends_on("Parsing", "Context-Free Grammars")
    O.add_depends_on("Shortest Path", "Priority Queue")
    O.add_depends_on("Spanning Tree", "Sorting")
    O.add_depends_on("Hash Table", "Hashing")
    O.add_depends_on("Transport Layer", "Network Layer")
    O.add_depends_on("Language Modeling", "Machine Learning")
    O.add_depends_on("Virtual Memory", "Computer Architecture")

    # Instances (≥2 per leaf)
    inst = O.add_instance
    inst("DFA", "Finite Automata")
    inst("NFA", "Finite Automata")
    inst("LL(1) grammar", "Context-Free Grammars")
    inst("LR(1) grammar", "Context-Free Grammars")
    inst("P problems", "Complexity Classes")
    inst("NP-complete problems", "Complexity Classes")

    inst("Haskell", "Functional Programming")
    inst("OCaml", "Functional Programming")
    inst("Java", "Object-Oriented Programming")
    inst("C++", "Object-Oriented Programming")
    inst("DFA scanner", "Lexical Analysis")
    inst("Regex-based scanner", "Lexical Analysis")
    inst("LL parser", "Parsing")
    inst("LR parser", "Parsing")

    inst("Dijkstra", "Shortest Path")
    inst("Bellman–Ford", "Shortest Path")
    inst("Kruskal", "Spanning Tree")
    inst("Prim", "Spanning Tree")
    inst("Merge sort", "Sorting")
    inst("Quick sort", "Sorting")

    inst("AVL tree", "Binary Search Tree")
    inst("Red–Black tree", "Binary Search Tree")
    inst("Separate chaining table", "Hash Table")
    inst("Open addressing table", "Hash Table")

    inst("Binary heap", "Priority Queue")
    inst("Fibonacci heap", "Priority Queue")

    inst("Round Robin", "CPU Scheduling")
    inst("Priority scheduling", "CPU Scheduling")
    inst("Paging", "Virtual Memory")
    inst("Segmentation", "Virtual Memory")

    inst("ARMv8", "RISC")
    inst("RISC-V", "RISC")
    inst("x86", "CISC")
    inst("x86-64", "CISC")
    inst("AVX2", "SIMD")
    inst("NEON", "SIMD")
    inst("SMP (shared-memory)", "MIMD")
    inst("MPI cluster", "MIMD")

    inst("TCP", "Transport Layer")
    inst("UDP", "Transport Layer")
    inst("IPv4", "Network Layer")
    inst("IPv6", "Network Layer")

    inst("MySQL", "Relational Databases")
    inst("PostgreSQL", "Relational Databases")
    inst("Redis", "Key–Value Stores")
    inst("DynamoDB", "Key–Value Stores")

    inst("AES-256", "Symmetric Cryptography")
    inst("ChaCha20", "Symmetric Cryptography")
    inst("RSA-2048", "Public-Key Cryptography")
    inst("ECDSA-P256", "Public-Key Cryptography")

    inst("Linear Regression", "Supervised Learning")
    inst("SVM", "Supervised Learning")
    inst("K-Means", "Unsupervised Learning")
    inst("PCA", "Unsupervised Learning")
    inst("n-gram model", "Language Modeling")
    inst("Transformer LM", "Language Modeling")

    inst("Delaunay triangulation", "Triangulation")
    inst("Ear clipping", "Triangulation")

    O.validate()
    return O


def demo(O: Ontology):
    print("== Demo queries ==")
    print("Depth from 'Computer Science':", O.max_depth_from("Computer Science"))
    print('is_a("Binary Search Tree", "Data Structures")  ->', O.is_a("Binary Search Tree", "Data Structures"))
    print('part_of("CPU Scheduling", "Operating Systems") ->', O.part_of("CPU Scheduling", "Operating Systems"))
    print('depends_on("Parsing", "Context-Free Grammars")->', O.depends_on("Parsing", "Context-Free Grammars"))
    path = O.any_path("Lexical Analysis", "Finite Automata")
    print('path "Lexical Analysis" -> "Finite Automata":', path)


def repl(O: Ontology):
    print("\n== REPL ==")
    print("Commands:")
    print('  isa "A" "B"        | part "A" "B"       | dep "A" "B"')
    print('  path "A" "B"       | instances "Class"  | classof "Instance"')
    print('  quit')
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            continue
        if line.lower() in {"quit", "exit"}:
            break
        try:
            toks = shlex.split(line)
        except ValueError as e:
            print("Parse error:", e)
            continue
        if not toks:
            continue
        cmd = toks[0].lower()

        def need(n):
            if len(toks) != n + 1:
                raise ValueError(f"{cmd} needs {n} arguments")

        try:
            if cmd == "isa":
                need(2)
                print(O.is_a(toks[1], toks[2]))
            elif cmd == "part":
                need(2)
                print(O.part_of(toks[1], toks[2]))
            elif cmd == "dep":
                need(2)
                print(O.depends_on(toks[1], toks[2]))
            elif cmd == "path":
                need(2)
                print(O.any_path(toks[1], toks[2]))
            elif cmd == "instances":
                need(1)
                print(O.instances_of(toks[1]))
            elif cmd == "classof":
                need(1)
                print(O.class_of(toks[1]))
            else:
                print("Unknown command.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    O = load_ontology()
    # demo(O)
    repl(O)


