from odoo import models, fields, api
from odoo.exceptions import UserError


class PlanSaleOrder(models.Model):
    _name = "plan.sale.order"
    _description = "Sale Plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    approver_ids = fields.Many2many("res.partner", string="Người duyệt")
    sale_order_id = fields.Many2one("sale.order", string="Mẫu báo giá", readonly=True)
    name = fields.Char(string="Tiêu đề", required=True)  # tiêu đề của kế hoạch
    # sale_order_id = fields.Many2one(
    #     "sale.order", string="Mẫu báo giá", readonly=True
    # )  # mẫu báo giá
    plan_sale_order_info = fields.Text(
        string="Thông tin kế hoạch",  default="Nội dung mặc định"
    )  # thông tin kế hoạch
    state = fields.Selection(
        [
            ("draft", "Nháp"),
            ("pending", "chờ phê duyệt"),
            ("approved", "Duyệt Kế hoạch"),
            ("rejected", "Từ chối"),
        ],
        string="Trạng thái",
        default="pending",
    )

    def action_confirm(self):
        for rec in self:
            rec.state = "approved"
            rec.message_post(body="Kế hoạch đã được duyệt", message_type="notification")
            rec.activity_schedule(
                "mail.mail_activity_data_todo",
                summary="Theo dõi kế hoạch bán hàng",
                user_id=self.env.user.id,
                note="kế hoạch này đã được duyệt, bạn cần theo dõi",
            )
        return True
            

    def action_cancel(self):   
        for rec in self:
            rec.state = "rejected"
            rec.message_post(body="Kế hoạch đã bị hủy", message_type="notification")
            rec.activity_unlink(["mail.mail_activity_data_todo"])
        return True
    
    def action_sent_for_approval(self):
        if not self.approver_ids:
            raise UserError("Vui lòng chọn ít nhất một người duyệt")
    
        self.state = "pending"  # Cập nhật trạng thái thành "pending"
        self.message_post(
            body=f"Kế hoạch bán hàng{self.name} đã được gửi cho người duyệt",
            message_type="notification",
        )
    # Gửi thông báo cho tất cả các người duyệt
        for approver in self.approver_ids:
            self.message_post(
            body=f"Bạn cần phê duyệt kế hoạch bán hàng: {self.name}",
            message_type='notification',  # Đảm bảo rằng đây là thông báo
            partner_ids=[approver.id],  # Gửi thông báo đến người duyệt
        )
        
        # Lên lịch hoạt động nếu cần (không bắt buộc)
        #     self.activity_schedule(
        #     'mail.mail_activity_data_todo',
        #     summary='Phê duyệt kế hoạch bán hàng',
        #     user_id=approver.id,
        #     note=f"Bạn cần phê duyệt kế hoạch bán hàng: {self.name}",
        # )

    
    