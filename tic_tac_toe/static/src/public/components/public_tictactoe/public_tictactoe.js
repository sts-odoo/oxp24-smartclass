import { Component, xml, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { TicTacToe } from "@tic_tac_toe/tictactoe/tictactoe"
import { rpc } from "@web/core/network/rpc";
import { user } from "@web/core/user";

class PublicTicTacToe extends Component {
    static template = xml`
        <TicTacToe game="game" clickSquare.bind="clickSquare"/>
    `;
    static components = { TicTacToe };

    setup() {
        this.game = useState({
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
        });
        this.orm = useService("orm");
        this.effect = useService("effect");
        this.bus = useService("bus_service");
        onWillStart(async () => {
            const result = await this.orm.call(
                "tictactoe.game",
                "current_state",
                [this.props.gameId],
                []
            );
            this._updateGameFromState(result);

        });
        this.bus.addChannel(this.props.gameId.toString());
        this.bus.subscribe("tic_tac_toe", (payload) => {
            Object.assign(this.game, payload);
        });
    }

    _updateGameFromState(state) {
        for (const position of Object.keys(this.game)) {
            const rec = state.play_ids.find((r) => r.position === position);
            if (rec) {
                this.game[position] = rec.player_id[0] === state.player_x_id[0] ? "X" : "O";
            } else {
                this.game[position] = "";
            }
        }
    }

    async clickSquare(position) {
        const result = await rpc("/tictactoe/"+ this.props.gameId+"/play", { position });
        this._updateGameFromState(result);
        if (result.winner_id && user.userId === result.winner_id[0]) {
            this.effect.add({message: "Congrats, You win !"})
        }
    }

}

registry.category("public_components").add("tictactoe.public_tictactoe", PublicTicTacToe);
