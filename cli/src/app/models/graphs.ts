export interface Edge {
    directed: boolean;
    label: string;
    source: number;
    target: number;
    weight: number;
}

export interface Node {
    label: string;
}

export interface Path {
    from: number;
    to: number;
    weight: number;
    weight_rule: number;
}

export interface Explanation {
    path: Path[];
    target: number;
    type: string;
    weight: number;
}

export interface Cause {
    edges: Edge[];
    label: string;
    paths: Explanation[];
    nodes: {[node: number]: Node}
}

export interface Graph {
    graph: Cause;
}

export interface Graphs {
    graphs: Graph[];
    label: string;
}