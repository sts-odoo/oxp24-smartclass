import { Component } from "@odoo/owl";

export class TicTacToe extends Component {
    static template = "tic_tac_toe.TicTacToe";
    static props = {
        game: { 
            type: Object, 
            shape: { 
                1: [{ value: "" }, { value: "X" }, { value: "O" }],
                2: [{ value: "" }, { value: "X" }, { value: "O" }],
                3: [{ value: "" }, { value: "X" }, { value: "O" }],
                4: [{ value: "" }, { value: "X" }, { value: "O" }],
                5: [{ value: "" }, { value: "X" }, { value: "O" }],
                6: [{ value: "" }, { value: "X" }, { value: "O" }],
                7: [{ value: "" }, { value: "X" }, { value: "O" }],
                8: [{ value: "" }, { value: "X" }, { value: "O" }],
                9: [{ value: "" }, { value: "X" }, { value: "O" }],
            } 
        },
        clickSquare: { type: Function, optional: true },
    };
    static defaultProps = {
        clickSquare: () => {},
    }
}