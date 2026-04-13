/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class BakeryDashboard extends Component {
    static template = "bakery_management.BakeryDashboard";

    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");

        this.state = useState({
            loading: true,
            orders_today: 0,
            revenue_this_month: 0,
            pending_orders: 0,
            low_stock_count: 0,
        });

        onWillStart(async () => {
            await this._loadDashboardData();
        });
    }

    async _loadDashboardData() {
        // TODO: implement full data loading with ORM calls
        this.state.loading = false;
    }
}

registry.category("actions").add("bakery.dashboard", BakeryDashboard);