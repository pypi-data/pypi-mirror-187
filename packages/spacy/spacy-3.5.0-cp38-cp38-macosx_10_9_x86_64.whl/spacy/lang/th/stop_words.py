STOP_WORDS = set(
    """
ทั้งนี้ ดัง ขอ รวม หลังจาก เป็น หลัง หรือ ๆ เกี่ยวกับ ซึ่งได้แก่ ด้วยเพราะ ด้วยว่า ด้วยเหตุเพราะ
ด้วยเหตุว่า สุดๆ เสร็จแล้ว เช่น เข้า ถ้า ถูก ถึง ต่างๆ ใคร เปิดเผย ครา รือ ตาม ใน ได้แก่ ได้แต่
ได้ที่ ตลอดถึง นอกจากว่า นอกนั้น จริง อย่างดี ส่วน เพียงเพื่อ เดียว จัด ทั้งที ทั้งคน ทั้งตัว ไกลๆ
ถึงเมื่อใด คงจะ ถูกๆ เป็นที นับแต่ที่ นับแต่นั้น รับรอง ด้าน เป็นต้นมา ทุก กระทั่ง กระทำ จวบ ซึ่งก็ จะ
ครบครัน นับแต่ เยอะๆ เพียงไหน เปลี่ยนแปลง ไป่ ผ่านๆ เพื่อที่ รวมๆ กว้างขวาง เสียยิ่ง เปลี่ยน ผ่าน
ทรง ทว่า กันเถอะ เกี่ยวๆ ใดๆ ครั้งที่ ครั้งนั้น ครั้งนี้ ครั้งละ ครั้งหลัง ครั้งหลังสุด ร่วมกัน ร่วมด้วย ก็ตามที
ที่สุด ผิดๆ ยืนยง เยอะ ครั้งๆ ใครๆ นั่นเอง เสมือนว่า เสร็จ ตลอดศก ทั้งที่ ยืนยัน ด้วยที่ บัดนี้
ด้วยประการฉะนี้ ซึ่งกัน ตลอดทั่วถึง ตลอดทั่วทั้ง ตลอดปี เป็นการ นั่นแหละ พร้อม เถิด ทั้ง สืบเนื่อง ตั้งแต่
กลับ กล่าวคือ กลุ่มก้อน กลุ่มๆ ครั้งครา ส่ง รวดเร็ว เสร็จสิ้น เสีย เสียก่อน เสียจน อดีต ตั้ง เกิด อาจ
อีก ตลอดเวลา ภายหน้า ภายหลัง มอง มันๆ มองว่า มัก มักจะ มัน หาก คงอยู่ เป็นที่ เป็นที่สุด
เป็นเพราะเป็นเพราะว่า เกี่ยวกัน เพียงไร เป็นแต่เพียง กล่าว จนบัดนี้ เป็นอัน จน จนเมื่อ จนแม้ ใกล้
ใหม่ๆ เป็นเพียง อย่างที่ ถูกต้อง ทั้งนั้น ทั้งนั้นด้วย กันดีกว่า กันดีไหม นั่นไง ตรงๆ แยะๆ เป็นต้น ใกล้ๆ
ซึ่งๆ ด้วยกัน ดังเคย เถอะ เสมือนกับ ไป คือ ขณะนี้ นอกจาก เพื่อที่จะ ขณะหนึ่ง ขวาง ครัน อยาก ไว้
แบบ นอกจากนี้ เนื่องจาก เดียวกัน คง ให้มา อนึ่ง ก็แล้วแต่ ต้อง ข้าง เพื่อว่า จนแม้น ครั้งหนึ่ง อะไร ซึ่ง
เกินๆ ด้วยเหตุนั้น กันและกัน รับ ระหว่าง ครั้งไหน เสร็จกัน ถึงอย่างไร ขาด ข้าฯ เข้าใจ ครบ ครั้งใด
ครบถ้วน ระยะ ไม่ เกือบ เกือบจะ เกือบๆ แก่ แก อย่างโน้น ดังกับว่า จริงจัง เยอะแยะ นั่น ด้วย ถึงแม้ว่า
มาก ตลอดกาลนาน ตลอดระยะเวลา ตลอดจน ตลอดไป เป็นอันๆ เป็นอาทิ ก็ต่อเมื่อ สู่ เมื่อ เพื่อ ก็ กับ
ด้วยเหมือนกัน ด้วยเหตุนี้ ครั้งคราว ราย ร่วม เป็นอันมาก สูง รวมกัน รวมทั้ง ร่วมมือ เป็นเพียงว่า รวมถึง
ต่อ นะ กว้าง มา ครับ ตลอดทั้ง การ นั้นๆ น่า เป็นอันว่า เพราะ วัน จนขณะนี้ จนตลอด จนถึง ข้า อย่างใด
ไหนๆ ก่อนหน้านี้ ก่อนๆ สูงกว่า สูงส่ง สูงสุด สูงๆ เสียด้วย เสียนั่น เสียนี่ เสียนี่กระไร เสียนั่นเอง สุด
สําหรับ ว่า ลง ภายใต้ เพื่อให้ ภายนอก ภายใน เฉพาะ ซึ่งกันและกัน ง่าย ง่ายๆ ไง ถึงแม้จะ ถึงเมื่อไร
เกิน ก็ได้ คราใด คราที่ ตลอดวัน นับ ดังเก่า ดั่งเก่า หลาย หนึ่ง ถือว่า ก่อนหน้า นับตั้งแต่ จรด จริงๆ
จวน จวนเจียน ตลอดมา กลุ่ม กระนั้น ข้างๆ ตรง ข้าพเจ้า กว่า เกี่ยวเนื่อง ขึ้น ให้ไป ผล แต่ เอง เห็น
จึง ได้ ให้ โดย จริงๆจังๆ ดั่งกับว่า ทั้งนั้นเพราะ นอก นอกเหนือ น่ะ กันนะ ขณะเดียวกัน แยะ
นอกเหนือจาก น้อย ก่อน จวนจะ ข้างเคียง ก็ตามแต่ จรดกับ น้อยกว่า นั่นเป็น นักๆ ครั้งกระนั้น เลย ไกล
สิ้นกาลนาน ครั้ง รือว่า เก็บ อย่างเช่น บาง ดั่ง ดังกล่าว ดังกับ รึ รึว่า ออก แรก จง ยืนนาน ได้มา ตน
ตนเอง ได้รับ ระยะๆ กระผม กันไหม กันเอง กำลังจะ กำหนด กู กำลัง ความ แล้ว และ ต่าง อย่างน้อย
อย่างนั้น อย่างนี้ ก็คือ ก็แค่ ด้วยเหตุที่ ใหญ่ๆ ให้ดี ยัง เป็นเพื่อ ก็ตาม ผู้ ต่อกัน ถือ ซึ่งก็คือ ภายภาค
ภายภาคหน้า ก็ดี ก็จะ อยู่ เสียยิ่งนัก ใหม่ ขณะ เริ่ม เรา ขวางๆ เสียแล้ว ใคร่ ใคร่จะ ตนฯ ของ แห่ง
รวด ดั่งกับ ถึงเมื่อ น้อยๆ นับจากนั้น ตลอด ตลอดกาล เสร็จสมบูรณ์ เขียน กว้างๆ ยืนยาว ถึงแก่ ขณะใด
ขณะใดๆ ขณะที่ ขณะนั้น จนทั่ว ภาคฯ ภาย เป็นแต่ อย่าง พบ ภาค ให้แด่ เสียจนกระทั่ง เสียจนถึง
จนกระทั่ง จนกว่า ตลอดทั่ว เป็นๆ นอกจากนั้น ผิด ครั้งก่อน แก้ไข ขั้น กัน ช่วง จาก รวมด้วย เขา
ด้วยเช่นกัน นอกจากที่ เป็นต้นไป ข้างต้น ข้างบน ข้างล่าง ถึงจะ ถึงบัดนั้น ถึงแม้ มี ทาง เคย นับจากนี้
อย่างเดียว เกี่ยวข้อง นี้ นํา นั้น ที่ ทําให้ ทํา ครานั้น ครานี้ คราหนึ่ง คราไหน คราว คราวก่อน คราวใด
คราวที่ คราวนั้น คราวนี้ คราวโน้น คราวละ คราวหน้า คราวหนึ่ง คราวหลัง คราวไหน คราวๆ คล้าย
คล้ายกัน คล้ายกันกับ คล้ายกับ คล้ายกับว่า คล้ายว่า ควร ค่อน ค่อนข้าง ค่อนข้างจะ ค่อยไปทาง ค่อนมาทาง ค
่อย ค่อยๆ คะ ค่ะ คำ คิด คิดว่า คุณ คุณๆ เคยๆ แค่ แค่จะ แค่นั้น แค่นี้ แค่เพียง แค่ว่า แค่ไหน จังๆ
จวบกับ จวบจน จ้ะ จ๊ะ จะได้ จัง จัดการ จัดงาน จัดแจง จัดตั้ง จัดทำ จัดหา จัดให้ จับ จ้า จ๋า จากนั้น
จากนี้ จากนี้ไป จำ จำเป็น จำพวก จึงจะ จึงเป็น จู่ๆ ฉะนั้น ฉะนี้ ฉัน เฉกเช่น เฉย เฉยๆ ไฉน ช่วงก่อน ช
่วงต่อไป ช่วงถัดไป ช่วงท้าย ช่วงที่ ช่วงนั้น ช่วงนี้ ช่วงระหว่าง ช่วงแรก ช่วงหน้า ช่วงหลัง ช่วงๆ ช่วย ช้า
ช้านาน ชาว ช้าๆ เช่นก่อน เช่นกัน เช่นเคย เช่นดัง เช่นดังก่อน เช่นดังเก่า เช่นดังที่ เช่นดังว่า
เช่นเดียวกัน เช่นเดียวกับ เช่นใด เช่นที่ เช่นที่เคย เช่นที่ว่า เช่นนั้น เช่นนั้นเอง เช่นนี้ เช่นเมื่อ เช่นไร
เชื่อ เชื่อถือ เชื่อมั่น เชื่อว่า ใช่ ใช้ ซะ ซะก่อน ซะจน ซะจนกระทั่ง ซะจนถึง ดั่งเคย ต่างก็ ต่างหาก
ตามด้วย ตามแต่ ตามที่ ตามๆ เต็มไปด้วย เต็มไปหมด เต็มๆ แต่ก็ แต่ก่อน แต่จะ แต่เดิม แต่ต้อง แต่ถ้า
แต่ทว่า แต่ที่ แต่นั้น แต่เพียง แต่เมื่อ แต่ไร แต่ละ แต่ว่า แต่ไหน แต่อย่างใด โต โตๆ ใต้ ถ้าจะ ถ้าหาก
ทั้งปวง ทั้งเป็น ทั้งมวล ทั้งสิ้น ทั้งหมด ทั้งหลาย ทั้งๆ ทัน ทันใดนั้น ทันที ทันทีทันใด ทั่ว ทำให้ ทำๆ ที ที่จริง
ที่ซึ่ง ทีเดียว ทีใด ที่ใด ที่ได้ ทีเถอะ ที่แท้ ที่แท้จริง ที่นั้น ที่นี้ ทีไร ทีละ ที่ละ ที่แล้ว ที่ว่า ที่แห่งนั้น ทีๆ ที่ๆ
ทุกคน ทุกครั้ง ทุกครา ทุกคราว ทุกชิ้น ทุกตัว ทุกทาง ทุกที ทุกที่ ทุกเมื่อ ทุกวัน ทุกวันนี้ ทุกสิ่ง ทุกหน ทุกแห่ง
ทุกอย่าง ทุกอัน ทุกๆ เท่า เท่ากัน เท่ากับ เท่าใด เท่าที่ เท่านั้น เท่านี้ แท้ แท้จริง เธอ นั้นไว นับแต่นี้
นาง นางสาว น่าจะ นาน นานๆ นาย นำ นำพา นำมา นิด นิดหน่อย นิดๆ นี่ นี่ไง นี่นา นี่แน่ะ นี่แหละ นี้แหล่
นี่เอง นี้เอง นู่น นู้น เน้น เนี่ย เนี่ยเอง ในช่วง ในที่ ในเมื่อ ในระหว่าง บน บอก บอกแล้ว บอกว่า บ่อย
บ่อยกว่า บ่อยครั้ง บ่อยๆ บัดดล บัดเดี๋ยวนี้ บัดนั้น บ้าง บางกว่า บางขณะ บางครั้ง บางครา บางคราว
บางที บางที่ บางแห่ง บางๆ ปฏิบัติ ประกอบ ประการ ประการฉะนี้ ประการใด ประการหนึ่ง ประมาณ
ประสบ ปรับ ปรากฏ ปรากฏว่า ปัจจุบัน ปิด เป็นด้วย เป็นดัง ผู้ใด เผื่อ เผื่อจะ เผื่อที่ เผื่อว่า ฝ่าย ฝ่ายใด
พบว่า พยายาม พร้อมกัน พร้อมกับ พร้อมด้วย พร้อมทั้ง พร้อมที่ พร้อมเพียง พวก พวกกัน พวกกู พวกแก
พวกเขา พวกคุณ พวกฉัน พวกท่าน พวกที่ พวกเธอ พวกนั้น พวกนี้ พวกนู้น พวกโน้น พวกมัน พวกมึง พอ พอกัน
พอควร พอจะ พอดี พอตัว พอที พอที่ พอเพียง พอแล้ว พอสม พอสมควร พอเหมาะ พอๆ พา พึง พึ่ง พื้นๆ พูด
เพราะฉะนั้น เพราะว่า เพิ่ง เพิ่งจะ เพิ่ม เพิ่มเติม เพียง เพียงแค่ เพียงใด เพียงแต่ เพียงพอ เพียงเพราะ
มากกว่า มากมาย มิ มิฉะนั้น มิใช่ มิได้ มีแต่ มึง มุ่ง มุ่งเน้น มุ่งหมาย เมื่อก่อน เมื่อครั้ง เมื่อครั้งก่อน
เมื่อคราวก่อน เมื่อคราวที่ เมื่อคราว เมื่อคืน เมื่อเช้า เมื่อใด เมื่อนั้น เมื่อนี้ เมื่อเย็น เมื่อวันวาน เมื่อวาน
แม้ แม้กระทั่ง แม้แต่ แม้นว่า แม้ว่า ไม่ค่อย ไม่ค่อยจะ ไม่ค่อยเป็น ไม่ใช่ ไม่เป็นไร ไม่ว่า ยก ยกให้ ยอม
ยอมรับ ย่อม ย่อย ยังคง ยังงั้น ยังงี้ ยังโง้น ยังไง ยังจะ ยังแต่ ยาก ยาว ยาวนาน ยิ่ง ยิ่งกว่า ยิ่งขึ้น
ยิ่งขึ้นไป ยิ่งจน ยิ่งจะ ยิ่งนัก ยิ่งเมื่อ ยิ่งแล้ว ยิ่งใหญ่ เร็ว เร็วๆ เราๆ เรียก เรียบ เรื่อย เรื่อยๆ ล้วน
ล้วนจน ล้วนแต่ ละ ล่าสุด เล็ก เล็กน้อย เล็กๆ เล่าว่า แล้วกัน แล้วแต่ แล้วเสร็จ วันใด วันนั้น วันนี้ วันไหน
สบาย สมัย สมัยก่อน สมัยนั้น สมัยนี้ สมัยโน้น ส่วนเกิน ส่วนด้อย ส่วนดี ส่วนใด ส่วนที่ ส่วนน้อย ส่วนนั้น ส
่วนมาก ส่วนใหญ่ สั้น สั้นๆ สามารถ สำคัญ สิ่ง สิ่งใด สิ่งนั้น สิ่งนี้ สิ่งไหน สิ้น แสดง แสดงว่า หน หนอ หนอย
หน่อย หมด หมดกัน หมดสิ้น หากแม้ หากแม้น หากแม้นว่า หากว่า หาความ หาใช่ หารือ เหตุ เหตุผล เหตุนั้น
เหตุนี้ เหตุไร เห็นแก่ เห็นควร เห็นจะ เห็นว่า เหลือ เหลือเกิน เหล่า เหล่านั้น เหล่านี้ แห่งใด แห่งนั้น
แห่งนี้ แห่งโน้น แห่งไหน แหละ ให้แก่ ใหญ่ ใหญ่โต อย่างมาก อย่างยิ่ง อย่างไรก็ อย่างไรก็ได้ อย่างไรเสีย
อย่างละ อย่างหนึ่ง อย่างๆ อัน อันจะ อันได้แก่ อันที่ อันที่จริง อันที่จะ อันเนื่องมาจาก อันละ อันๆ อาจจะ
อาจเป็น อาจเป็นด้วย อื่น อื่นๆ เอ็ง เอา ฯ ฯล ฯลฯ 555 กำ ขอโทษ เยี่ยม นี่คือ
""".split()
)
