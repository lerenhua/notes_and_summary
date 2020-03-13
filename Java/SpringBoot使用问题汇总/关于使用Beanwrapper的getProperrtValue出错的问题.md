在自定义constraints时,需要implement一个validator,其中关键一个是要实现isValid方法,问题代码如下:
```Java
@Override
    public boolean isValid(Object value, ConstraintValidatorContext context) {

        if (null == value) {
            return true;
        }

        BeanWrapperImpl beanWrapper = new BeanWrapperImpl(value);
        if (beanWrapper.isReadableProperty(startTime)) {
            System.out.println("数据可读");
        }
        Object start = beanWrapper.getPropertyValue(startTime);
        Object end = beanWrapper.getPropertyValue(endTime);

        if (null == start || null == end) {
            return true;
        }
        int result = ((Date) end).compareTo((Date) start);

        if (result >= 0) {
            return true;
        }
        return  false;
    }
```
这是一段用于实现一个数据实体中两个时间字段是否合法的代码, 其中引用变量value指向的对象就是使用了注解的数据实体对象,为了代码复用,不对value指向的对象特定化,所以使用BeanWrapper类来获取value指向对象的字段信息.<br>数据实体类的定义代码如下:
```Java
/*   修改信息的校验检查  */
@CheckIntervalTime(stratTime = "in_cote_time", endTime = "out_cote_time", message = "出栏或死亡时间不能早于入栏时间")
public class ModifyDataVal {
    @NotNull(message = "id编号不能为空")
    public  Integer id;        // 羊数据库中自动生成的编号
    @NotNull(message = "RFID编号不能为空")
    public  String rfid;       // RFID编号
    @NotNull(message = "物种不能为空")
    public Integer species;    //  物种
    @NotNull(message = "入栏时间不能为空")
    public Date in_cote_time;  //  入栏时间


    public Date out_cote_time; // 出栏或死亡时间

    public Integer mother_id;  // 母亲id编号
    public Integer father_id;  // 父亲id编号
    @NotNull(message = "羊舍编号不能为空")
    @Min(value = 1, message = "羊舍编号不能小于1")
    public Integer cote_id;    // 所在羊舍编号
    public String desc;        // 描述
}
```

出现错误位置是getPropertyValue方法异常,报错:对应字段不可读或没有正确的get方法.<br>
经排查,在定义数据实体类时,必须要给出对于实例变量的get方法,所以在实体类中需要添加如下代码:
```java
    public Date getIn_cote_time() {
        return in_cote_time;
    }
     public Date getOut_cote_time() {
        return out_cote_time;
    }
```

总结: 出现错误首先根据报错理解可能出现的问题,再去一个个排查.还有,在springboot中有很多这样在我看来是隐式的操作,比如实现数据库的接口Repo时,只需声明一个类似于findById这样的方法,就可以自动实现相应功能,这种自动化必要要求标准化,所以存在一些编写代码的潜在要求,需留意.
