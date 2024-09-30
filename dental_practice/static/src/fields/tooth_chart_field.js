import { Component, } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { ToothChart } from "../tooth_chart/tooth_chart";

class ToothChartField extends Component {
    static template = "dental_practice.ToothChartField";
    static props = {
        ...standardFieldProps,
    };
    static components = { ToothChart };

    setup() {
        this.tooth = {
            11: { color: 0 },
            12: { color: 0 },
            13: { color: 0 },
            14: { color: 0 },
            15: { color: 0 },
            16: { color: 0 },
            17: { color: 0 },
            18: { color: 0 },
            21: { color: 0 },
            22: { color: 0 },
            23: { color: 0 },
            24: { color: 0 },
            25: { color: 0 },
            26: { color: 0 },
            27: { color: 0 },
            28: { color: 0 },
            31: { color: 0 },
            32: { color: 0 },
            33: { color: 0 },
            34: { color: 0 },
            35: { color: 0 },
            36: { color: 0 },
            37: { color: 0 },
            38: { color: 0 },
            41: { color: 0 },
            42: { color: 0 },
            43: { color: 0 },
            44: { color: 0 },
            45: { color: 0 },
            46: { color: 0 },
            47: { color: 0 },
            48: { color: 0 },
        };
    }
}

const toothChartField = {
    component: ToothChartField,
    displayName: _t("ToothChartField"),
    supportedTypes: ["one2many"],
    isEmpty: () => false,
};

registry.category("fields").add("tooth_chart", toothChartField);
