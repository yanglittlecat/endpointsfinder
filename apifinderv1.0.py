# -*- coding: utf-8 -*-
from burp import IBurpExtender, IContextMenuFactory, ITab
from java.awt import BorderLayout, Font
from javax.swing import JPanel, JScrollPane, JTextArea, JMenuItem, JButton, JLabel
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class BurpExtender(IBurpExtender,IContextMenuFactory,ITab):
        #插件注册
        def registerExtenderCallbacks(self,callbacks):
            self._callbacks = callbacks
            self._helpers = callbacks.getHelpers()
            self._callbacks.setExtensionName("Juicy Points")
            self._callbacks.registerContextMenuFactory(self)

            self.endpoints = set()

            self._init_ui()
            self._callbacks.addSuiteTab(self)
            self._print(u"loaded!")

        def _init_ui(self):
            layout = BorderLayout()
            self.main_panel = JPanel(layout)

            self.output_area = JTextArea()
            self.output_area.setFont(Font(u"Microsoft YaHei", Font.PLAIN, 12))
            scroll_pane = JScrollPane(self.output_area)

            #控制面板
            control_panel = JPanel()


            self.copy_btn = JButton(u'copy all', actionPerformed=self.copy_all)
            self.clear_btn = JButton(u'clear', actionPerformed=self.clear_results)

            control_panel.add(JLabel(u'juicy endpoints:'))
            control_panel.add(self.copy_btn)
            control_panel.add(self.clear_btn)

            #添加到主件
            self.main_panel.add(control_panel, BorderLayout.NORTH)
            self.main_panel.add(scroll_pane, BorderLayout.CENTER)
        #右键选项注册
        def createMenuItems(self,invocation):
            return [JMenuItem("find endpoints",actionPerformed=lambda x, inv=invocation: self._bulk_extract(inv))]

        def _bulk_extract(self,invocation):
            self.endpoints.clear()
            total = 0

            for msg in invocation.getSelectedMessages():
                if msg.getResponse():
                    response_raw = msg.getResponse()
                    response_info = self._helpers.analyzeResponse(response_raw)
                    body_offset = response_info.getBodyOffset()
                    body_bytes = msg.getResponse()[body_offset:]
                    response_info_body = self._helpers.bytesToString(body_bytes)
                    found = self.extract_all(response_info_body)
                    if found: total+=1

            #输出结果到面板上
            self.output_area.setText(u"\n".join(list(self.endpoints)))

            self._print(u"founded {} endpoints".format(total))

        def _print(self,text):
            try:
                print(text)
            except:
                print(text.encode('utf-8'))

        def extract_all(self,response_body):
            found = False
            #提取正则
            endpoints_pattern = r'(?:"|\')(/(?!\d+$)[\w\-/]+)(?:"|\')'
            for match in re.findall(endpoints_pattern, response_body):
                    if (match.startswith("/")
                        and not re.match(r"^/\d+$", match)
                        and not re.match(r"^//", match)
                        and not re.match(r"(\.(?:js|png|css|jpg|gif|ico|svg|woff2?|ttf|mp4|pdf))", match)):#排除脏乱路径
                        self.endpoints.add(match)
                        found = True
            return found


        def clear_results(self,event):
            self.output_area.setText(u"")
            self.endpoints.clear()

        def copy_all(self, event):
            self.output_area.selectAll()
            self.output_area.copy()
            self._callbacks.issusAlert(u"复制成功")

        def getTabCaption(self):
            return "Juicy endPoints"

        def getUiComponent(self):
            return self.main_panel