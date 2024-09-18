import { Component, onWillUnmount, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useRecordObserver } from "@web/model/relational_model/utils";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { TicTacToe } from "../tictactoe/tictactoe"
import { user } from "@web/core/user";

class TicTacToeField extends Component {
    static template = "tic_tac_toe.TicTacToeField";
    static props = {
        ...standardFieldProps
    };
    static components = { TicTacToe };

    setup() {
        this.playerX;
        this.playerO;
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
        this.notification = useService("notification");
        this.effect = useService("effect");
        this.bus = useService("bus_service");
        useRecordObserver((record) => {
            this.playerX = record.data.player_x_id;
            this.playerO = record.data.player_o_id;
            const recs = record.data[this.props.name].records;
            for (const position of Object.keys(this.game)) {
                const rec = recs.find((r) => r.data.position === position);
                if (rec) {
                    this.game[position] = rec.data.player_id[0] === this.playerX[0] ? "X" : "O";
                } else {
                    this.game[position] = "";
                }
              }
        });
        this.busCallBack = () => this.props.record.load();
        this.bus.addChannel(this.props.record.data.id.toString());
        this.bus.subscribe("tic_tac_toe", this.busCallBack);
        onWillUnmount(() => {
            this.bus.deleteChannel(this.props.record.data.id.toString());
            this.bus.unsubscribe("tic_tac_toe", this.busCallBack);
        })
    }

    get list() {
        return this.props.record.data[this.props.name];
    }

    async clickSquare(position) {
        if (this.props.record.model.root.dirty) {
            this.notification.add("You should save, before play");
            return;
        }
        if (this.props.record.data.next_player_id && !this.list.records.some((r) => r.data.position === position)) {
            const params = {
                context: {
                    default_position: position,
                    default_player_id: this.props.record.data.next_player_id["0"],
                },
            };
            await this.list.addNewRecord(params);
            await this.props.record.model.root.save();
            if (this.props.record.data.winner_id && user.userId === this.props.record.data.winner_id[0]) {
                this.effect.add({message: "Congrats, You win !"})
            }
        }
    }
}

const ticTacToeField = {
    component: TicTacToeField,
    displayName: _t("Tic-Tac-Toe"),
    supportedTypes: ["one2many"],
    isEmpty: () => false,
    relatedFields: () => {
        return [
            { name: "player_id", type: "many2one", relation: "res.users", readonly: false },
            { name: "position", type: "selection", selection: [
                ["1", _t("Top Left")],
                ["2", _t("Top Center")],
                ["3", _t("Top Right")],
                ["4", _t("Middle Left")],
                ["5", _t("Middle Center")],
                ["6", _t("Middle Right")],
                ["7", _t("Bottom Left")],
                ["8", _t("Bottom Center")],
                ["9", _t("Bottom Right")],
            ], readonly: false },
            { name: "sequence", type: "integer", readonly: false },
        ];
    },
};

registry.category("fields").add("tic_tac_toe", ticTacToeField);
