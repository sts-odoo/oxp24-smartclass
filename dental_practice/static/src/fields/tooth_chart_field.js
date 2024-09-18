/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { formatDate } from "@web/core/l10n/dates";
import { ToothChart } from "../tooth_chart/tooth_chart";
import { useService } from "@web/core/utils/hooks";
import { useRecordObserver } from "@web/model/relational_model/utils";
import { deepCopy } from "@web/core/utils/objects";

class ToothChartField extends Component {
    static template = "dental_practice.ToothChartField";
    static props = {
        ...standardFieldProps,
    };
    static components = { ToothChart };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.tooth = useState({});
        useRecordObserver((record) => {
            // clean the tooths.
            this.tooth[11] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[12] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[13] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[14] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[15] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[16] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[17] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[18] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[21] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[22] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[23] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[24] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[25] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[26] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[27] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[28] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[31] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[32] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[33] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[34] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[35] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[36] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[37] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[38] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[41] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[42] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[43] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[44] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[45] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[46] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[47] = { color: 0, tooltipInfo: { data: [] } };
            this.tooth[48] = { color: 0, tooltipInfo: { data: [] } };

            this.records = [...record.data[this.props.name].records].reverse();
            for (const rec of this.records) {
                if (["tooth", "part"].includes(rec.data.dental_care_type)) {
                    this.tooth[rec.data.dental_tooth].color = rec.data.color;
                    this.tooth[rec.data.dental_tooth].tooltipInfo.data.push({
                        id: rec.id,
                        name: rec.data.name,
                        date: formatDate(rec.data.date),
                        dental_position: rec.data.dental_position,
                    });
                }
            }
        });
    }

    get toothData() {
        const toothData = deepCopy(this.tooth);
        // tooltipInfo should be a JSON !
        Object.keys(toothData).forEach( (teeth) => toothData[teeth].tooltipInfo = JSON.stringify(toothData[teeth].tooltipInfo));
        return toothData;
    }

    toothSelected(tooth) {
        this.action.doAction({
            name: _t("Intervention"),
            type: "ir.actions.act_window",
            res_model: "dental.intervention.wizard",
            views: [[false, "form"]],
            view_mode: "form",
            target: "new",
            context: {
                default_partner_id: this.props.record.resId,
                default_dental_tooth: tooth.toString(),
            }},{
                onClose: () => {
                    this.props.record.load();
                },
            });
    }
}

const toothChartField = {
    component: ToothChartField,
    displayName: _t("ToothChartField"),
    supportedTypes: ["one2many"],
    isEmpty: () => false,
    relatedFields: () => {
        return [
               { name: "name", type: "char" },
               { name: "date", type: "date" },
               { name: "product_id", type: "many2one", relation: "product.product" },
               { name: "partner_id", type: "many2one", relation: "res.partner" },
               { name: "dental_tooth", type: "integer" },
               { name: "color", type: "integer" },
               { name: "dental_care_type", type: "select" },
               { name: "dental_position", type: "selection", selection: [
                    ["outside", _t("Outside")],
                    ["top", _t("Top")],
                    ["inside", _t("Inside")],
                ]},
        ];
    },
};

registry.category("fields").add("tooth_chart", toothChartField);
