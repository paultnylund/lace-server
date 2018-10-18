class Graph {
    constructor() {
        this.ADJ_MATRIX = [];
    }

    initialise(vertices) {
        const array = [];
        
        for (let i = 0; i < vertices; i += 1) {
            array.push(0);
            this.ADJ_MATRIX.push(array);
        }
    };

    calculateWeight(density) {

    };

    addWeightedEdge(vertex1, vertex2, weight) {
        this.ADJ_MATRIX[vertex1][vertex2] = weight;
    };

    createDummyData(size) {
        const weight = (min, max) => {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        };

        for (let i = 0; i < size; i += 1) {
            const array = [];
            for (let j = 0; j < size; j += 1) {
                array[j] = weight(0, 10);
            }

            this.ADJ_MATRIX[i] = array;
        }
    }

    create(size) {
        const weight = (min, max) => {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        };

        for (let i = 0; i < size; i += 1) {
            for (let j = 0; j < size; j += 1) {
                graph.addWeightedEdge(i, j, weight(0, 10));
            }
        }
    };
};
