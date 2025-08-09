# -*- coding: utf-8 -*-
from burp import IBurpExtender, IContextMenuFactory, ITab
from java.awt import BorderLayout, Font
from javax.swing import (
    JPanel, JScrollPane, JTextArea, JMenuItem,
    JButton, JLabel, JTabbedPane
)
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class BurpExtender(IBurpExtender, IContextMenuFactory, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._callbacks.setExtensionName("Juicy Points")
        self._callbacks.registerContextMenuFactory(self)

        self.endpoints = set()
        self.emails = set()
        self.phones = set()

        self._init_ui()
        self._callbacks.addSuiteTab(self)
        self._print(u"loaded!")

    def _init_ui(self):
        self.main_panel = JTabbedPane()

        # Endpoint 页面
        self.endpoint_area = JTextArea()
        self.endpoint_area.setFont(Font(u"Microsoft YaHei", Font.PLAIN, 12))
        self.endpoint_panel = self._build_tab_panel(
            self.endpoint_area, self.copy_endpoints, self.clear_endpoints
        )
        self.main_panel.addTab("📍 Endpoints (0)", self.endpoint_panel)

        # Email 页面
        self.email_area = JTextArea()
        self.email_area.setFont(Font(u"Microsoft YaHei", Font.PLAIN, 12))
        self.email_panel = self._build_tab_panel(
            self.email_area, self.copy_emails, self.clear_emails
        )
        self.main_panel.addTab("📧 Emails (0)", self.email_panel)

        # Phone 页面
        self.phone_area = JTextArea()
        self.phone_area.setFont(Font(u"Microsoft YaHei", Font.PLAIN, 12))
        self.phone_panel = self._build_tab_panel(
            self.phone_area, self.copy_phones, self.clear_phones
        )
        self.main_panel.addTab("📱 Phones (0)", self.phone_panel)

    def _build_tab_panel(self, text_area, copy_action, clear_action):
        panel = JPanel(BorderLayout())
        control = JPanel()
        copy_btn = JButton(u'copy all', actionPerformed=copy_action)
        clear_btn = JButton(u'clear', actionPerformed=clear_action)
        control.add(copy_btn)
        control.add(clear_btn)
        panel.add(control, BorderLayout.NORTH)
        panel.add(JScrollPane(text_area), BorderLayout.CENTER)
        return panel

    def createMenuItems(self, invocation):
        return [JMenuItem("find endpoints", actionPerformed=lambda x, inv=invocation: self._bulk_extract(inv))]

    def _bulk_extract(self, invocation):
        self.endpoints.clear()
        self.emails.clear()
        self.phones.clear()
        total = 0

        for msg in invocation.getSelectedMessages():
            if msg.getResponse():
                response_raw = msg.getResponse()
                response_info = self._helpers.analyzeResponse(response_raw)
                body_offset = response_info.getBodyOffset()
                body_bytes = response_raw[body_offset:]
                response_body = self._helpers.bytesToString(body_bytes)

                total += self.extract_all(response_body)

        # 更新UI文本
        self.endpoint_area.setText(u"\n".join(sorted(self.endpoints)))
        self.email_area.setText(u"\n".join(sorted(self.emails)))
        self.phone_area.setText(u"\n".join(sorted(self.phones)))

        # 更新 tab 标题
        self.main_panel.setTitleAt(0, u"📍 Endpoints ({})".format(len(self.endpoints)))
        self.main_panel.setTitleAt(1, u"📧 Emails ({})".format(len(self.emails)))
        self.main_panel.setTitleAt(2, u"📱 Phones ({})".format(len(self.phones)))

        self._print(u"发现 {} 条 endpoints，{} 个邮箱，{} 个手机号".format(
            len(self.endpoints), len(self.emails), len(self.phones)
        ))

    def extract_all(self, response_body):
        found = 0

        # 提取 endpoints
        endpoints_pattern = r'(?:"|\')(/(?!\d+$)[\w\-/]+)(?:"|\')'
        for match in re.findall(endpoints_pattern, response_body):
            if (match.startswith("/")
                    and not re.match(r"^/\d+$", match)
                    and not re.match(r"^//", match)
                    and not re.search(r"(\.(?:js|png|css|jpg|gif|ico|svg|woff2?|ttf|mp4|pdf))$", match)):
                self.endpoints.add(match)
                found += 1

        # 提取邮箱
        email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        for email in re.findall(email_pattern, response_body):
            self.emails.add(email)

        # 提取中国手机号
        phone_pattern = r"(?<![\d\w])1[3-9]\d{9}(?![\d\w])"
        for phone in re.findall(phone_pattern, response_body):
            self.phones.add(phone)

        return found

    def clear_endpoints(self, event): self.endpoint_area.setText(""); self.endpoints.clear(); self.main_panel.setTitleAt(0, "📍 Endpoints (0)")
    def clear_emails(self, event): self.email_area.setText(""); self.emails.clear(); self.main_panel.setTitleAt(1, "📧 Emails (0)")
    def clear_phones(self, event): self.phone_area.setText(""); self.phones.clear(); self.main_panel.setTitleAt(2, "📱 Phones (0)")

    def copy_endpoints(self, event): self.endpoint_area.selectAll(); self.endpoint_area.copy()
    def copy_emails(self, event): self.email_area.selectAll(); self.email_area.copy()
    def copy_phones(self, event): self.phone_area.selectAll(); self.phone_area.copy()

    def _print(self, text):
        try:
            print(text)
        except:
            print(text.encode('utf-8'))

    def getTabCaption(self):
        return "Juicy Scanner"

    def getUiComponent(self):
        return self.main_panel


