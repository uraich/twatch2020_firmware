#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from gui.icon import Icon

class Calculator():
    op1_text="0"
    op2_text="0"
    op_num=0

    digits="0123456789"
    operators=["+","-","x","/"]
    dec_point = False
    operator = None
    resultFlag = False
    btnm_map = ["7","8", "9", "/", " ","\n",
                "4", "5", "6", "x", lv.SYMBOL.BACKSPACE, "\n",
                "1", "2", "3","+","=","\n",
                "c","0",".","-"," ",""]

    btnm_ctlr_map = [lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.HIDDEN,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.NO_REPEAT,
                     lv.btnmatrix.CTRL.HIDDEN]

    def __init__(self,mainbar):
        try:
            import ulogging as logging
        except:
            import logging
             
        self.log = logging.getLogger("CalculatorApp")
        self.log.setLevel(logging.DEBUG)
        
        self.mainbar=mainbar
        self.statusbar=mainbar.gui.statusbar
        self.app = mainbar.app
        
        self.tile_num = mainbar.add_app_tile( 1, 1, "calculator app" )
        self.log.debug("tile number for main tile: %d",self.tile_num)
        
        self.log.debug("registering calculator app")
        app=self.app.register("calculator","calculator_64px",self.enter_calculator_app_event_cb)
        self.main_page(self.tile_num)
        
    def main_page(self,tile_num):
        self.calculator_tile = self.mainbar.get_tile_obj(tile_num);
        self.calculator_style = lv.style_t()
        self.calculator_style.copy(self.mainbar.get_style())
        
         # create the number textarea
        self.ta = lv.textarea(self.calculator_tile,None)
        self.ta.set_size(200,40)
        self.ta.align(None,lv.ALIGN.IN_TOP_MID,0,10)
        self.ta.set_text("0")

        # create a button matrix
        self.btnm = lv.btnmatrix(self.calculator_tile,None)
        self.btnm.set_map(self.btnm_map)
        self.btnm.set_ctrl_map(self.btnm_ctlr_map)
        self.btnm.set_width(226)
        self.btnm.align(self.ta,lv.ALIGN.OUT_BOTTOM_MID,0,10)
        # attach the callback
        self.btnm.set_event_cb(self.event_handler)
        # create the exit button
        
        exit_btn = lv.imgbtn(self.calculator_tile,None)        
        exit_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.add_style(lv.imgbtn.PART.MAIN,self.calculator_style)
        exit_btn.align(self.calculator_tile,lv.ALIGN.IN_BOTTOM_LEFT, 10, -10 )
        self.log.debug("setting up exit callback")
        exit_btn.set_event_cb(self.exit_calculator_app_event_cb)
        
        self.calculator_style.set_text_opa(lv.obj.PART.MAIN, lv.OPA.COVER)
            
    def enter_calculator_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("enter_calculator_app_event_cb called")
            self.statusbar.hide(True)
            # self.app.hide_indicator( example_app )
            self.mainbar.jump_to_tilenumber(self.tile_num, lv.ANIM.OFF )
            
    def exit_calculator_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("exit_calculator_app_event_cb called")
            self.statusbar.hide(False)
            self.mainbar.jump_to_maintile(lv.ANIM.OFF)
    
    def event_handler(self,source,evt):

        if evt == lv.EVENT.VALUE_CHANGED:
            print("Toggled")
            txt = source.get_active_btn_text()
            #
            # treat digits
            #
            if txt in self.digits:
                print("digit: ",txt)
                if self.resultFlag:
                    self.op_num = 0
                    self.resultFlag = False
                    self.op1_text="0"
                    self.op2_text="0"
                if self.op_num == 0:
                    if self.op1_text == "0":
                        self.op1_text = txt
                    else:
                        self.op1_text = self.op1_text + txt
                    self.ta.set_text(self.op1_text)                    
                else:
                    if self.op2_text == "0":
                        self.op2_text = txt
                    else:
                        self.op2_text = self.op2_text + txt                
                    self.ta.set_text(self.op2_text)

            #
            # treat decimal point
            #
            elif txt == ".":
                if self.dec_point:
                    print ("decimal point was already typed")
                    return
                else:
                    print("decimal point")
                    self.dec_point=True
                if self.op_num == 0:
                    self.op1_text = self.op1_text + txt
                    self.ta.set_text(self.op1_text)
                else:
                    self.op2_text = self.op2_text + txt
                    self.ta.set_text(self.op2_text)
                    
            elif txt == lv.SYMBOL.BACKSPACE:
                print("backspace")
                if self.op_num == 0:
                    if self.op1_text == "0":
                        return
                    else:
                        removedChar = self.op1_text[-1:]
                        if removedChar == '.':
                            self.dec_point = False
                        self.op1_text = self.op1_text[:-1]
                        self.ta.set_text(self.op1_text)
                else:
                    if self.op2_text == "0":
                        return
                    else:
                        removedChar = self.op2_text[-1:]
                        if removedChar == '.':
                            self.dec_point = False
                        self.op2_text = self.op2_text[:-1]
                        self.ta.set_text(self.op2_text)                   
                    
            elif txt == "c":
                print("clear")
                if self.op_num == 0:
                    self.op1_text = "0"
                    self.ta.set_text(self.op1_text)
                else:
                    self.op2_text = "0"
                    self.ta.set_text(self.op2_text)
                operator=None
                dec_point=False
            
            elif txt == "=":
                print("Calculate result of operation: ",self.op1_text,self.operator,self.op2_text)
                if self.operator in self.operators:
                    op1 = float(self.op1_text)
                    op2 = float(self.op2_text)
                    print("op1: %f, op2: %f"%(op1,op2))
                    if self.operator == "+":
                        print(op1,self.operator,op2)                    
                        result = op1 + op2
                        res_text = str(result)
                        self.op2_text = "0"
                        self.op1_text = res_text
                        print(op1,self.operator,op2)
                    
                    elif self.operator == "-":
                        print(op1,self.operator,op2)                    
                        result = op1 - op2
                        res_text = str(result)
                        self.op2_text = "0"
                        self.op1_text = res_text

                    elif self.operator == "x":
                        print(op1,self.operator,op2)                    
                        result = op1 * op2
                        res_text = str(result)
                        self.op2_text = "0"
                        self.op1_text = res_text
                        
                    elif self.operator == "/":
                        print(op1,self.operator,op2)  
                        if op2 == 0:
                            res_text = "NaN"
                        else:
                            result = op1 / op2
                            res_text = str(result)
                            self.op2_text = "0"
                            self.op1_text = res_text
                            
                    print("result text: ", res_text)    
                    self.ta.set_text(res_text)
                    self.operator = None
                    self.resultFlag=True
                    if res_text == "NaN":
                        self.resultFlag=False
                        self.op1_text="0"
                        self.op_num = 0
                        self.op2_text="0"
                
            else:
                print("Operator: ",txt)
                self.resultFlag=False
                if self.operator:
                    print("operator already selected")
                else:
                    self.op_num=1
                    self.dec_point=False
                    self.operator = txt
                    self.ta.set_text(self.op2_text)
