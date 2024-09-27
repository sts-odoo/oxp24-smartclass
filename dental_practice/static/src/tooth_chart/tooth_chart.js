/** @odoo-module **/

import { Component } from "@odoo/owl";

const TOOTH_SHAPE = {
    type: Object,
    shape: {
        color: [{ value: 0 }, { value: 1 }, { value: 2 }, { value: 3 }, { value: 4 }, { value: 5 }, { value: 6 }, { value: 7 }, { value: 8 }, { value: 9 }, { value: 10 }, { value: 11 }],
        tooltipInfo: { type: String, optional: true },
        },
    };

export class ToothChart extends Component {
    static template = "dental_practice.ToothChart";
    static props = {
        tooth: {
            type: Object,
            shape: {
                11: TOOTH_SHAPE,
                12: TOOTH_SHAPE,
                13: TOOTH_SHAPE,
                14: TOOTH_SHAPE,
                15: TOOTH_SHAPE,
                16: TOOTH_SHAPE,
                17: TOOTH_SHAPE,
                18: TOOTH_SHAPE,
                21: TOOTH_SHAPE,
                22: TOOTH_SHAPE,
                23: TOOTH_SHAPE,
                24: TOOTH_SHAPE,
                25: TOOTH_SHAPE,
                26: TOOTH_SHAPE,
                27: TOOTH_SHAPE,
                28: TOOTH_SHAPE,
                31: TOOTH_SHAPE,
                32: TOOTH_SHAPE,
                33: TOOTH_SHAPE,
                34: TOOTH_SHAPE,
                35: TOOTH_SHAPE,
                36: TOOTH_SHAPE,
                37: TOOTH_SHAPE,
                38: TOOTH_SHAPE,
                41: TOOTH_SHAPE,
                42: TOOTH_SHAPE,
                43: TOOTH_SHAPE,
                44: TOOTH_SHAPE,
                45: TOOTH_SHAPE,
                46: TOOTH_SHAPE,
                47: TOOTH_SHAPE,
                48: TOOTH_SHAPE,
            }
        },
        tooltipTemplate: { type: String, optional: true },
        toothSelected: { type: Function, optional: true },
    };

    static defaultProps = {
        toothSelected: () => {},
    }
}
