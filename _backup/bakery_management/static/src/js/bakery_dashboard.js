/** @odoo-module **/
/**
 * Bakery Dashboard — Tableau de bord Pâtisserie
 * Composant OWL pour Odoo 17
 */
import { registry }    from "@web/core/registry";
import { useService }  from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class BakeryDashboard extends Component {
    static template = "bakery_management.BakeryDashboard";

    setup() {
        this.orm           = useService("orm");
        this.actionService = useService("action");

        this.state = useState({
            loading:             true,
            orders_today:        0,
            orders_this_month:   0,
            revenue_this_month:  0,
            pending_orders:      0,
            low_stock_count:     0,
            recent_orders:       [],
            low_stock_items:     [],
        });

        onWillStart(async () => {
            await this._loadDashboardData();
        });
    }

    // ─── Helpers date ─────────────────────────────────────────────────────

    _dateStr(d) {
        const pad = (n) => String(n).padStart(2, "0");
        return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
    }

    // ─── Chargement des données ───────────────────────────────────────────

    async _loadDashboardData() {
        const now        = new Date();
        const todayStart = this._dateStr(now) + " 00:00:00";
        const monthStart = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-01 00:00:00`;

        try {
            // Commandes aujourd'hui
            this.state.orders_today = await this.orm.searchCount(
                "bakery.order",
                [["date_order", ">=", todayStart], ["state", "not in", ["cancelled"]]],
            );

            // Commandes ce mois
            this.state.orders_this_month = await this.orm.searchCount(
                "bakery.order",
                [["date_order", ">=", monthStart], ["state", "not in", ["cancelled"]]],
            );

            // CA ce mois (commandes livrées)
            const doneOrders = await this.orm.searchRead(
                "bakery.order",
                [["date_order", ">=", monthStart], ["state", "=", "done"]],
                ["amount_total"],
                { limit: 2000 },
            );
            this.state.revenue_this_month = doneOrders.reduce(
                (sum, o) => sum + o.amount_total, 0
            );

            // Commandes en cours
            this.state.pending_orders = await this.orm.searchCount(
                "bakery.order",
                [["state", "in", ["confirmed", "production", "ready"]]],
            );

            // Stock faible / vide
            this.state.low_stock_count = await this.orm.searchCount(
                "bakery.ingredient",
                [["stock_status", "in", ["low", "empty"]]],
            );

            // Commandes récentes
            this.state.recent_orders = await this.orm.searchRead(
                "bakery.order",
                [["state", "not in", ["cancelled"]]],
                ["name", "partner_id", "amount_total", "state", "date_order", "date_delivery"],
                { limit: 8, order: "date_order desc" },
            );

            // Ingrédients stock faible
            this.state.low_stock_items = await this.orm.searchRead(
                "bakery.ingredient",
                [["stock_status", "in", ["low", "empty"]]],
                ["name", "quantity_on_hand", "minimum_quantity", "unit_of_measure", "stock_status"],
                { limit: 6 },
            );
        } catch (e) {
            console.error("BakeryDashboard: erreur de chargement", e);
        } finally {
            this.state.loading = false;
        }
    }

    // ─── Formatters ───────────────────────────────────────────────────────

    formatCurrency(amount) {
        return new Intl.NumberFormat("fr-MA", {
            style:                 "currency",
            currency:              "MAD",
            minimumFractionDigits: 2,
        }).format(amount);
    }

    formatDate(dateStr) {
        if (!dateStr) return "—";
        // Les dates Odoo sont en "YYYY-MM-DD HH:MM:SS"
        const [datePart, timePart] = dateStr.split(" ");
        const [y, m, d] = datePart.split("-");
        const [hh, mm]  = (timePart || "00:00").split(":");
        return `${d}/${m}/${y} ${hh}:${mm}`;
    }

    getStateLabel(state) {
        return {
            draft:      "Brouillon",
            confirmed:  "Confirmée",
            production: "En production",
            ready:      "Prête",
            done:       "Livrée",
            cancelled:  "Annulée",
        }[state] || state;
    }

    getStateClass(state) {
        return {
            draft:      "bk-state-draft",
            confirmed:  "bk-state-confirmed",
            production: "bk-state-production",
            ready:      "bk-state-ready",
            done:       "bk-state-done",
            cancelled:  "bk-state-cancelled",
        }[state] || "";
    }

    // ─── Navigation ───────────────────────────────────────────────────────

    async openOrders() {
        await this.actionService.doAction("bakery_management.action_bakery_order");
    }

    async openIngredients() {
        await this.actionService.doAction("bakery_management.action_bakery_ingredient");
    }

    async openLowStock() {
        await this.actionService.doAction("bakery_management.action_bakery_low_stock");
    }

    async openPendingOrders() {
        await this.actionService.doAction({
            type:      "ir.actions.act_window",
            name:      "Commandes en cours",
            res_model: "bakery.order",
            views:     [[false, "list"], [false, "form"]],
            domain:    [["state", "in", ["confirmed", "production", "ready"]]],
        });
    }

    async openOrder(orderId) {
        await this.actionService.doAction({
            type:      "ir.actions.act_window",
            res_model: "bakery.order",
            res_id:    orderId,
            views:     [[false, "form"]],
            target:    "current",
        });
    }

    async openNewOrder() {
        await this.actionService.doAction({
            type:      "ir.actions.act_window",
            name:      "Nouvelle commande",
            res_model: "bakery.order",
            views:     [[false, "form"]],
            target:    "current",
            context:   {},
        });
    }

    async openProducts() {
        await this.actionService.doAction("bakery_management.action_bakery_product");
    }

    async openCustomers() {
        await this.actionService.doAction("bakery_management.action_bakery_customer");
    }
}

registry.category("actions").add("bakery.dashboard", BakeryDashboard);
